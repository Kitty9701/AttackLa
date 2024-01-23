import argparse
import ruamel.yaml as YAML

def read_yaml(yaml_file):
    """
    Read the input yaml file entered by the user
    """
    yaml = YAML.YAML(typ='rt')
    with open(yaml_file) as file:
        config = yaml.load(file)
    print(config)
    return config

def main(config):
    file = open("attack.py", "w")
    file.write("import numpy as np\n")
    file.write("from PIL import Image\n")
    file.write("import cv2\n")
    
    file.write('def Attack(data):\n')
    if(config['attack name']=="Black screen attack"):
        file.write('    data = np.zeros(data.shape, dtype=np.uint8)\n')
        
    if(config['attack name']=="Strong light exposure attack"):
        percentage = config['impact']['influence']['luminance']
        file.write('    data = cv2.cvtColor(data, cv2.COLOR_RGB2YUV)\n')
        file.write('    h = data.shape[0]\n')
        file.write('    w = data.shape[1]\n')
        file.write('    for i in range(h):\n')
        file.write('        for j in range(w):\n')
        file.write('            y = data[i][j][0]*'+str(float(percentage[:-1]) / 100.0)+'\n')
        file.write('            if y > 255:\n')
        file.write('                y = 255\n')
        file.write('            data[i][j][0] = int(y)\n')
        file.write('    data = cv2.cvtColor(data, cv2.COLOR_YUV2RGB)\n')
    
    if(config['attack name']=="Laser beam attack"):
        file.write('    laser_pattern = cv2.imread("laser_for_carriage.png")\n')
        file.write('    if laser_pattern is None:\n')
        file.write('        print("read image fail!!")\n')
        file.write('        return 0\n')
        file.write('    laser_pattern = cv2.cvtColor(laser_pattern, cv2.COLOR_BGR2RGB)\n')
        file.write('    data = data.astype(np.float32)\n')
        file.write('    laser_pattern = laser_pattern.astype(np.float32)\n')
        file.write('    data = cv2.addWeighted(data, 1.0 , laser_pattern, 1.0 , 0)\n')
        file.write('    data = np.clip(data, 0.0, 255.0).astype("uint8")\n')
    file.write('    return data\n')
    file.close()
    print("done")

if __name__ == '__main__':
    description = "CARLA Attack Generation\n"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--attack_description_file', type=str, default="attack3.yml", help='Type the attack description file path')
    args = parser.parse_args()
    config = read_yaml(args.attack_description_file)
    main(config)
