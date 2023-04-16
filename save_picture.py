import os
import cv2
from matplotlib import pyplot as plt
import matplotlib.image as mping
from detect import light_detect

img_path = r'D:\jetbrains\project\python\project2\pictures_new'
path = './pictures_new'
imgs = os.listdir(img_path)

for i in imgs:
    # name.append(i)
    pth = os.path.join(path, i)
    # img_path = os.path.join('D:\jetbrains\project\python\project2\pictures', i)
    # txt.write(name+'\n')
    img = mping.imread(pth)
    print("{}".format(i))
    k = light_detect(img)
    # print(img_size)
    if k < 0.85:
        plt.imsave("./pictures_point/{}".format(i), img)
    else:
        plt.imsave("./pictures_line/{}".format(i), img)
