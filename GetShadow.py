"""get the shadow proportion form images
   of remote sensing"""
import numpy as np
import cv2
import os
import glob
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.colors import LinearSegmentedColormap
from pylab import mpl
import random

mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False


def standard(data):
    ''' 影像文件标准化
       输入单通道影像
       输出标准化后单通道影像 '''
    mdata = data.copy()
    irow, icol = mdata.shape[0:2]
    mdata = np.reshape(mdata, [irow * icol, 1])
    temp1 = mdata - np.min(data)
    result = temp1 / (np.max(data) - np.min(data))
    result = np.reshape(result, [irow, icol])
    return result


def GetLight(img):
    '''计算人眼视觉特性亮度'''
    mimg = img.copy()
    B = mimg[:, :, 0]
    G = mimg[:, :, 1]
    R = mimg[:, :, 2]
    result = 0.04 * R + 0.5 * G + 0.46 * B
    return result


def GetColor(img):
    '''色度空间归一化'''
    mimg = img.copy()
    misc = mimg[:, :, 0] + mimg[:, :, 1] + mimg[:, :, 2]
    misc[misc == 0] = 0.0000001
    mimg[:, :, 0] = img[:, :, 0] / misc
    mimg[:, :, 1] = img[:, :, 1] / misc
    result = np.abs(mimg - img)
    result = (result[:, :, 0] + result[:, :, 1]) / 2
    return result


def GetVege(img):
    ''' 获取植被特征 '''
    mimg = img.copy()
    B = mimg[:, :, 0]
    G = mimg[:, :, 1]
    R = mimg[:, :, 2]
    result = G - np.minimum(R, B)
    result[result < 0] = 0
    return result


def GetLDV(idist, ilight, ivege):
    ''' 总决策 '''
    idist = standard(idist)
    ilight = standard(ilight)
    ivege = standard(ivege)
    result = idist - ilight - ivege
    result[result < 0] = 0
    return result


def FinalTrare(img):
    ''' 结果后处理 '''
    mimg = img.copy()
    mimg = np.uint8(standard(mimg) * 255)
    T, result = cv2.threshold(mimg, 0, 255, cv2.THRESH_OTSU)
    result = cv2.medianBlur(result, 7)
    return result


if __name__ == "__main__":
    # 获取输入图片路径
    filepath = './pictures_new/3.jpg'
    filenames = glob.glob(filepath + '*')
    print(filenames)
    for filename in filenames:
        img = cv2.imread(filename)
        # 获取阴影
        img1 = img.copy()
        img1 = img1.astype(np.float64)
        img1[:, :, 0] = standard(img1[:, :, 0])
        img1[:, :, 1] = standard(img1[:, :, 1])
        img1[:, :, 2] = standard(img1[:, :, 2])
        idist = GetColor(img1)
        ilight = GetLight(img1)
        ivege = GetVege(img1)
        final = GetLDV(idist, ilight, ivege)
        shadow = FinalTrare(final)
        # 可视化
        color_list = ['#00000000', '#4cb4e7']
        my_cmap = LinearSegmentedColormap.from_list('mcmp', color_list)
        matplotlib.colormaps.register(cmap=my_cmap)
        fig = plt.figure()
        plt.title('阴影提取结果', fontsize=12, fontweight='bold')
        plt.imshow(img)
        plt.imshow(shadow, cmap='mcmp')
    plt.show()
