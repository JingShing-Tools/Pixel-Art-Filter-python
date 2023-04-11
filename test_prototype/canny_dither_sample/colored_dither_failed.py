import cv2
import numpy as np
# It looks like 2077

# 讀取影像
img = cv2.imread('image/or.jpg')
scale = 3
h, w, c = img.shape
d_h = int(h / scale)
d_w = int(w / scale)
img = cv2.resize(img, (d_w, d_h), interpolation=cv2.INTER_NEAREST)
# Canny邊緣檢測
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 100, 200)

# 彩色Order Dither處理
dither_kernel = np.array([[0, 7, 3],
                          [6, 5, 2],
                          [4, 1, 8]]) / 9.0

h, w = edges.shape
for y in range(1, h-1):
    for x in range(1, w-1):
        if edges[y, x] > 0:
            patch = img[y-1:y+2, x-1:x+2, :]
            result = (patch > dither_kernel * 255).astype(np.uint8) * 255
            img[y-1:y+2, x-1:x+2, :] = result

img = cv2.resize(img, (d_w * scale, d_h * scale), interpolation=cv2.INTER_NEAREST)

# 顯示處理結果
cv2.imshow('output', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
