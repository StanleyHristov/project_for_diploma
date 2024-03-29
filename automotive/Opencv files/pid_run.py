import cv2
import numpy as np
import socket
from alexnet import alexnet
import os
import time

s = socket.socket()
host = '192.168.1.110'
port = 12345
s.connect((host, port))
cap = cv2.VideoCapture('http://192.168.1.104:81/stream')

speed = 300
last_pos = 0
w = 0
KP = .8
KD = 5
KI = .5
max_correction = 1000
WIDTH = 80
HEIGHT = 60
LR = 1e-3
EPOCHS = 10
MODEL_NAME = 'autonomous_car-{}-{}-{}-epochs.model'.format(LR, 'alexnetv2', EPOCHS)

model = alexnet(WIDTH, HEIGHT, LR)
model.load(MODEL_NAME)

def convert(x, i_m, i_M, o_m, o_M):
    return max(min(o_M, (x - i_m) * (o_M - o_m) // (i_M - i_m) + o_m), o_m)

def weighted(move):
    move.pop(1)
    avg_num = 0.0
    avg_den = 0.0
    for i in range(0, 2):
        avg_num += move[i] * i * 1000
        avg_den += move[i]
    return avg_num / avg_den

def correction(angle):
    if angle > 0:
        return min(angle, max_correction)
    else:
        return max(angle, -max_correction)

def servo_angle(z):
    if z > 0:
        steer_angle = convert(z, 0, 1000, 75, 89)
    else:
        steer_angle = convert(z, -1000, 0, 59, 75)
    return steer_angle

while True:
    ret, frame = cap.read()
    screen = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    screen = cv2.resize(screen, (80, 60))
    prediction = model.predict([screen.reshape(WIDTH, HEIGHT, 1)])[0]
    moves = list(np.around(prediction, decimals=2))
    w = convert(weighted(moves), 0, 1000, -500, 500)

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
    
    print(moves, st)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
