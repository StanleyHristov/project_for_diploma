import socket
import time
from pynput.keyboard import Listener
from log import key_check

s = socket.socket()
host = '192.168.137.142'
port = 12345

s.connect((host, port))

def key_out(key):
    output = [0, 0, 0, 0]
    if 'A' in key:
        output[0] = 1
    if 'D' in key:
        output[3] = 1
    if 'W' in key:
        output[1] = 1
    if 'S' in key:
        output[2] = 1
    return output

try:
    while True:
        key = key_check()
        a = key_out(key)
        x = '{"a":' + str(a[0]) + ',"d":' + str(a[3]) + ',"w":' + str(a[1]) + ',"s":' + str(a[2]) + "}"
        msg = str.encode(x, 'utf-8')
        print(msg)
        s.send(msg)
        data1 = s.recv(1024)

except KeyboardInterrupt:
    print('exit')
