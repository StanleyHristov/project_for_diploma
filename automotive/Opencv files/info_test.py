import numpy as np 
import pandas as pd
from random import shuffle
import cv2

train_data = np.load('trained.npy', allow_pickle=True)

for data in train_data:
    img = data[0]
    choice = data[1]
    img_resized = cv2.resize(img, (400, 300))
    cv2.imshow('test', img_resized)
    print(choice)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
