import cv2
import numpy as np

# 讀取圖像
img = cv2.imread('input_image.jpg')

# 將圖像轉為灰度
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 使用Canny邊緣檢測
edges = cv2.Canny(gray, 100, 200)

# 定義有序抖動的閾值矩陣
threshold = np.array([[0, 128], [192, 64]], dtype=np.uint8)

# 使用有序抖動處理邊緣
dithered_edges = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
dithered_edges = cv2.resize(dithered_edges, None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST)
dithered_edges = cv2.dither(dithered_edges, threshold)

# 將處理後的邊緣合併到原圖像中
output = cv2.bitwise_and(img, img, mask=dithered_edges)

# 顯示輸出圖像
cv2.imshow('output', output)
cv2.waitKey(0)
cv2.destroyAllWindows()
