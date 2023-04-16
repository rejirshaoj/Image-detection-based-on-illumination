import os
import cv2
from PIL import Image

# 文件夹路径
img_path = r'D:\jetbrains\project\python\project2\pictures'

# txt 保存路径
save_txt_path = r'./images.txt'
txt = open(save_txt_path, 'w')

# 读取文件夹中的所有文件
imgs = os.listdir(img_path)
# name = []

# 写入图片地址
for i in imgs:
    # name.append(i)
    pth = os.path.join('./pictures', i)
    # img_path = os.path.join('D:\jetbrains\project\python\project2\pictures', i)
    # txt.write(name+'\n')
    img_size = os.path.getsize(pth)
    # img_size /= 1024  # 除以1024是代表Kb
    # print(img_size)
    img = cv2.imread(pth)

    img2 = Image.open(pth)
    # x = img2.width
    # y = img2.height
    # x_1 = 3360  # 定义缩小后的标准宽度
    # y_1 = int(y * x_1 / x)  # 计算缩小后的高度
    out = img2.resize((3360, 2240), Image.Resampling.LANCZOS)  # 改变尺寸，保持图片高品质
    # # 判断图片的通道模式，若图片在RGBA模式下，需先将其转变为RGB模式
    # if out.mode == 'RGBA':
    #     # 转化为rgb格式
    #     out = out.convert('RGB')
    out.save("./pictures_new/{}".format(i))

    pth_new = os.path.join('./pictures_new', i)
    # cv2.imwrite('111.png', img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])

    txt.write(pth_new + '\n')

txt.close()

# path : 读取地址
# pth = os.path.join('./pictures', i)

# def save_point(path, img_path, save_txt_path):
#     imgs = os.listdir(img_path)
#     txt = open(save_txt_path, 'w')
#     for i in imgs:
#         # name.append(i)
#         pth = os.path.join(path, i)
#         # img_path = os.path.join('D:\jetbrains\project\python\project2\pictures', i)
#         # txt.write(name+'\n')
#         img_size = os.path.getsize(pth)
#         img_size /= 1024  # 除以1024是代表Kb
#         img = cv2.imread(pth)
#         # print(img_size)
#         if img_size > 2048:
#             img2 = Image.open(pth)
#             x = img2.width
#             y = img2.height
#             x_1 = 3360  # 定义缩小后的标准宽度
#             y_1 = int(y * x_1 / x)  # 计算缩小后的高度
#             out = img2.resize((x_1, y_1), Image.Resampling.LANCZOS)  # 改变尺寸，保持图片高品质
#             # # 判断图片的通道模式，若图片在RGBA模式下，需先将其转变为RGB模式
#             # if out.mode == 'RGBA':
#             #     # 转化为rgb格式
#             #     out = out.convert('RGB')
#             out.save("./pictures_point/{}".format(i))
#         else:
#             cv2.imwrite(r"./pictures_point/{}".format(i), img)
#         pth_new = os.path.join('./pictures_point', i)
#         # cv2.imwrite('111.png', img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
#
#         txt.write(pth_new + '\n')
#
#     txt.close()
