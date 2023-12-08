import numpy as np
from PIL import Image
import cv2

def LightExposureAttack(data):
    data = cv2.cvtColor(data, cv2.COLOR_RGB2YUV)
    h = data.shape[0]
    w = data.shape[1]
    for i in range(h):
        for j in range(w):
            y = data[i][j][0]*3
            if y > 255:
                y = 255
            data[i][j][0] = y
    data = cv2.cvtColor(data, cv2.COLOR_YUV2RGB)
    #Image.fromarray(data).save('light_exposure.png')
    return data

def main():
    print("test black screen attack")
    data = cv2.imread("test.png")
    data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
    print(data.shape)
    LightExposureAttack(data)
    
if __name__ == "__main__":
    main()
