import cv2
import numpy as np
import socket
from log import key_check
import os
import time
s = socket.socket()         # Create a socket object
host = 'IP_of_esp32'            
port = 12345                # Reserve a port for your service.
s.connect((host, port))


cap = cv2.VideoCapture('http://111.111.111.11:81/stream') #esp32cam ip stream. Check on esp32cam serial for ip
time.sleep(5)               #wait for 5 sec
print('start')

#creating file store data
file_name = 'training_data.npy'
if os.path.isfile(file_name):
    print("File exists , loading previous data")
    training_data = list(np.load(file_name, allow_pickle=True))
else:
    print('file does not exist, starting fresh')
    training_data = []

def key_out(key):
    output = [0, 0, 0, 0]
    if 'A' in key:
        output[0] = 1
    if 'D' in key:
        output[2] = 1
    if 'W' in key:
        output[1] = 1
    if 'S' in key:
        output[3] = 1
    return output
    


while(True):
    key = key_check()
    a = key_out(key)
    
    #create a serialized dict
    x = '{"a":'
    x += str(a[0])
    x += ',"d":'
    x += str(a[2])
    x += ',"w":'
    x += str(a[1])
    x += ',"s":'
    x += str(a[3])
    x += "}"
    msg = str.encode(x, 'utf-8')
    #print(msg)
    s.send(msg)
    data1 = s.recv(1024)
    ret, frame = cap.read()
    rotate = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE) #align the video feed 
    screen = cv2.cvtColor(rotate, cv2.COLOR_BGR2GRAY)
    screen = cv2.resize(screen, (80, 60))
    a.pop()
    #print(a)
    training_data.append([screen, a])
    cv2.imshow('rotate', rotate)
    cv2.imshow('screen', screen)
    #save data to file after every 500 data point collection
    if len(training_data) % 500 == 0:
        print(len(training_data))
        np.save(file_name, training_data)
    
   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
