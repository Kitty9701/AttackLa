import numpy as np
from PIL import Image
import cv2

def LaserBeamAttack(data):
    laser_pattern = cv2.imread("laser_for_carriage.png")
    if laser_pattern is None:
        print("read image fail!!")
        return 0
    laser_pattern = cv2.cvtColor(laser_pattern, cv2.COLOR_BGR2RGB)
    # laser_pattern = cv2.resize(laser_pattern, (data.shape[1], data.shape[0]))
    data = data.astype(np.float32)
    laser_pattern = laser_pattern.astype(np.float32)
    data = cv2.addWeighted(data, 1.0 , laser_pattern, 1.0 , 0)
    data = np.clip(data, 0.0, 255.0).astype('uint8')
    #Image.fromarray(data).save('laser_beam2.png')
    return data

def main():
    print("test laser beam attack")
    data = cv2.imread("test.png")
    data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
    print(data.shape)
    LaserBeamAttack(data)
    
if __name__ == "__main__":
    main()
