import cv2
import numpy as np

scale = 3
# 讀取圖像
img = cv2.imread('image/or.jpg')
h, w, c = img.shape
d_h = int(h / scale)
d_w = int(w / scale)
img = cv2.resize(img, (d_w, d_h), interpolation=cv2.INTER_NEAREST)
# 將圖像轉為灰度
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 使用Canny邊緣檢測
edges = cv2.Canny(gray, 100, 200)

# 定義有序抖動的閾值矩陣
threshold = np.array([[0, 128, 32], [192, 64, 224], [48, 160, 96]], dtype=np.uint8)

# 使用有序抖動處理邊緣
dithered_edges = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
dithered_edges = cv2.copyMakeBorder(dithered_edges, 1, 1, 1, 1, cv2.BORDER_REFLECT)
for i in range(1, dithered_edges.shape[0]-1):
    for j in range(1, dithered_edges.shape[1]-1):
        if dithered_edges[i, j] > threshold[i % 3, j % 3]:
            dithered_edges[i, j] = 255
        else:
            dithered_edges[i, j] = 0

# 將處理後的邊緣合併到原圖像中
img = cv2.bitwise_and(img, img, mask=dithered_edges[1:-1, 1:-1])

img = cv2.resize(img, (d_w * scale, d_h * scale), interpolation=cv2.INTER_NEAREST)

# 顯示輸出圖像
cv2.imshow('output', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
