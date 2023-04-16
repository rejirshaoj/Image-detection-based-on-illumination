from math import tan

import cv2
import numpy
import numpy as np
from matplotlib import pyplot as plt

from GetShadow import standard, GetColor, GetLight, GetVege, GetLDV, FinalTrare

img = cv2.imread("pictures_line/1.jpg")

img1 = img.astype(np.float64)
img1[:, :, 0] = standard(img[:, :, 0])
img1[:, :, 1] = standard(img[:, :, 1])
img1[:, :, 2] = standard(img[:, :, 2])
shadow = FinalTrare(GetLDV(GetColor(img1), GetLight(img1), GetVege(img1)))
m, n = shadow.shape

blur = cv2.GaussianBlur(img, (21, 21), 0)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

sift = cv2.SIFT_create()
kp = sift.detect(img)
kp_new = []  # 阴影范围特征点
# print(kp)


def near_shadow(pt: tuple) -> bool:
    x, y = pt
    x, y = round(x), round(y)
    for dx in range(-1, 1):
        if x + dx < 0:
            continue
        if x + dx >= n:
            break
        for dy in range(-1, 1):
            if y + dy < 0:
                continue
            if y + dy >= m:
                break
            if shadow[y + dy][x + dx] != 0:
                return True
    return False


for key_point in kp:
    if near_shadow(key_point.pt):
        kp_new.append(key_point)

# 阴影内特征点
cv2.drawKeypoints(gray, kp_new, blur, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
plt.figure(figsize=(m / 100, n / 100))
plt.imsave("figure1.png", blur)


# 分区域
sp_size = 4
row, col = 2, 2
assert row * col == sp_size

a, b = m // row, n // col
sp = []

# for i in range(sp_size):
#     x_start = i // col * a
#     y_start = i % col * b
#     sp.append(img1[x_start:x_start + a, y_start:y_start + b])


# 聚类
def cluster(i: int, kp_sift):

    angle, pt_cluster, weight, = [], [], []
    weight_size, cnt = 0, 0
    angle_new, pt_new_x, pt_new_y = 0, 0, 0

    x_start = i // col * a
    y_start = i % col * b

    for keypoint in kp_sift:
        if x_start <= keypoint.pt[0] <= x_start + a and y_start <= keypoint.pt[1] <= y_start + b:
            angle.append(keypoint.angle)
            pt_cluster.append(keypoint.pt)
            weight.append(keypoint.size)
            cnt += 1
            weight_size += keypoint.size

    for j in range(cnt):
        angle_new = angle_new + angle[j] * weight[j] / weight_size
        pt_new_x = pt_new_x + pt_cluster[j][0] * weight[j] / weight_size
        pt_new_y = pt_new_y + pt_cluster[j][1] * weight[j] / weight_size

    if cnt < 10:
        pt_new_x, pt_new_y, angle_new = 0, 0, 0

    return pt_new_x, pt_new_y, angle_new


keypoint_new = []

img2 = img
for i in range(sp_size):
    pt_x0, pt_x1 = 0, 3360
    keypoint_new.append(cluster(i, kp_new))
    k = tan(keypoint_new[i][2])
    pt_y0 = k * (pt_x0 - keypoint_new[i][0]) + keypoint_new[i][1]
    pt_y1 = k * (pt_x1 - keypoint_new[i][0]) + keypoint_new[i][1]
    cv2.line(img2, tuple(map(int, (pt_x0, pt_y0))), tuple(map(int, (pt_x1, pt_y1))), (0, 255, 0), thickness=3)

plt.imsave("figure2.png", img2)

#  print(keypoint_new)





