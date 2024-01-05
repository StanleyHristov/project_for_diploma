import json
import motor

def socet():
    import socket
    import time
    from machine import Pin, TouchPad, PWM

    p1 = Pin(13)
    servo = PWM(p1, freq=50)

    s = socket.socket()
    host = '192.168.1.110'
    port = 12345
    s.bind((host, port))
    s.listen(5)

    def convert(x, i_m, i_M, o_m, o_M):
        return max(min(o_M, (x - i_m) * (o_M - o_m) // (i_M - i_m) + o_m), o_m)

    def coneect():
        motor.motorSpeed(0)
        while True:
            c, addr = s.accept()
            print('Got connection from', addr)

            while True:
                d = "thank you for connection"
                data = str(d)
                msg = str.encode(data, 'utf-8')
                try:
                    c.send(msg)
                    a = c.recv(1024)
                    com = a.decode()
                    de = json.loads(com)  # deserialize incoming dictionary

                    if len(de) < 3:
                        angle = int(de['a'])
                        speed = int(de["w"])
                        servo.duty(angle)
                        print(angle, speed)
                        if abs(speed):
                            motor.motorSpeed(speed)
                        else:
                            motor.motorSpeed(0)
                    else:
                        if de["w"] == 1 and de["s"] == 0:
                            motor.motorSpeed(1000)
                        if de["s"] == 1 and de["w"] == 0:
                            motor.motorSpeed(-1000)
                        if de["a"] == 1 and de["d"] == 0:
                            servo.duty(55)
                        if de["d"] == 1 and de["a"] == 0:
                            servo.duty(89)
                        if de["d"] == 0 and de["a"] == 0:
                            servo.duty(75)
                        if de["w"] == 0 and de["s"] == 0:
                            motor.motorSpeed(0)
                        print(de)  # for debugging
                except:
                    connect()

    connect()
