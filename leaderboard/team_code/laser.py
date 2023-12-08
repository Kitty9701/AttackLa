import numpy as np
import math
import os
import torch
from light_simulation import tube_light_generation_by_func, simple_add
from torchvision.datasets import ImageFolder
from torchvision.models import resnet50
import torchvision.transforms as transforms
import argparse
import random
import shutil
import itertools
from tqdm import tqdm
from PIL import Image
import torchvision.transforms.functional as transf
import time
def AddLaser(np_img, model='resnet50', ifsave=False, save_dir='./results'):
    init_v = [394,40,13,32]
    radians = math.radians(init_v[1])
    k = round(math.tan(radians), 2)
    
    # t1 = time.time()
    tube_light = tube_light_generation_by_func(k, b=init_v[2], alpha = 1.0, beta=init_v[3], wavelength=init_v[0]) 
    tube_light =  tube_light * 255.0
    #tube_light = tube_light.astype(np.float32)
    #tube_light = np.clip(tube_light, 0.0, 255.0).astype('uint8')
    #Image.fromarray(tube_light).save('light.jpg')
    # t2 = time.time()
    
    img_with_light = simple_add(np_img, tube_light, 1.0)
    img_with_light = np.clip(img_with_light, 0.0, 255.0).astype('uint8')
    
    # save
    if ifsave:
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        Image.fromarray(img_with_light).save(os.path.join(save_dir, '3.jpg'))
        #print(search_i)
    
    # print(t1,t2-t1,time.time()-t2,time.time()-t0)
    return img_with_light
