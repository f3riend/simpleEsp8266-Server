import network
import socket
from machine import Pin, Timer


led = Pin(2, Pin.OUT)


ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='FakeWifi', password='12345678')
ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
ap.config(pm=0)


while not ap.active():
    pass
print('Ağ Aktif:', ap.ifconfig())


led_state = False 


def web_page():
    global led_state
    if led_state:
        gpio_state = "ON"
    else:
        gpio_state = "OFF"
    
    html = f"""
    <html>
    <head>
        <title>ESP8266 Web Server</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
        <h1>ESP8266 Web Server</h1>
        <p>LED State: {gpio_state}</p>
        <a href="/?led=on"><button>LED ON</button></a>
        <a href="/?led=off"><button>LED OFF</button></a>
    </body>
    </html>
    """
    return html


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)


def keep_alive(timer):
    pass 


timer = Timer(0)
timer.init(period=10000, mode=Timer.PERIODIC, callback=keep_alive)

while True:
    conn, addr = s.accept()
    print('Yeni bağlantı:', addr)
    request = conn.recv(1024)
    request = str(request)
    

    if '/?led=on' in request:
        print('LED AÇ')
        led_state = True  
        led.value(0)
    if '/?led=off' in request:
        print('LED KAPAT')
        led_state = False 
        led.value(1)
    

    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
