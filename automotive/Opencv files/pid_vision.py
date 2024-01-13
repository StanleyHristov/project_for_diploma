import cv2
import numpy as np
import time
import os 
import socket

s = socket.socket()
host = '192.168.1.110'
port = 12345
s.connect((host, port))

speed = 1000
last_pos = 0
w = 0
KP = 2
KD = 1.4
KI = .5
max_correction = 1000

def convert(x, i_m, i_M, o_m, o_M):
    return max(min(o_M, (x - i_m) * (o_M - o_m) // (i_M - i_m) + o_m), o_m)

def correction(angle):
    if angle > 0:
        return min(angle, max_correction)
    else:
        return max(angle, -max_correction)

def servo_angle(z):
    if z > 0:
        return convert(z, 0, 1000, 75, 89)
    else:
        return convert(z, -1000, 0, 59, 75)

cap = cv2.VideoCapture('http://192.168.1.104:81/stream')

while True:
    l = 0
    r = 0
    ret, frame = cap.read()
    screen = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    screen = cv2.resize(screen, (80, 60))
    kernel = np.ones((15,15), np.float32)/225
    smoothed = cv2.filter2D(frame, -1, kernel)
    low_b = np.uint8([55, 55, 55])
    high_b = np.uint8([0, 0, 0])
    mask = cv2.inRange(smoothed, high_b, low_b)
    contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            w = convert(cx, 0, 300, -500, 500)
            propotional_angle = int(w)
            derivative_angle = propotional_angle - last_pos
            integral_angle = propotional_angle + last_pos
            steer = (propotional_angle * KP + derivative_angle * KD + integral_angle * KI)
            z = int(correction(steer))
            st = servo_angle(z)
            x = '{"a":' + str(st) + ',"w":' + str(speed) + "}"
            msg = str.encode(x, 'utf-8')
            s.send(msg)
            data1 = s.recv(1024)
            last_pos = propotional_angle
    else:
        print("I don't see the line")
        x = '{"a":' + str(75) + ',"w":' + str(0) + "}"
        msg = str.encode(x, 'utf-8')
        s.send(msg)
        data1 = s.recv(1024)
    cv2.drawContours(frame, contours, -1, (0,255,0), 1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("QUIT")
        x = '{"a":' + str(75) + ',"w":' + str(0) + "}"
        msg = str.encode(x, 'utf-8')
        s.send(msg)
        data1 = s.recv(1024)
        break

cap.release()
cv2.destroyAllWindows()
