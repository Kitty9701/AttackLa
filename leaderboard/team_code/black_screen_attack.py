import numpy as np
from PIL import Image

def Black_screen_attack(data):
    data = np.zeros(data.shape, dtype=np.uint8)
    Image.fromarray(data).save('black.png')
    return data

def main():
    print("test black screen attack")
    data = np.ones((128,128,3),dtype=np.uint8)
    print(data)
    print(data.shape)
    Image.fromarray(data).save('black_before.png')
    Black_screen_attack(data)
    
if __name__ == "__main__":
    main()
