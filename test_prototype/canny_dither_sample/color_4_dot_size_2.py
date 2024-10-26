import cv2
import numpy as np

# 讀取原圖
image = cv2.imread('image/or.jpg')  # 這裡使用正確的檔案路徑
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 定義 4 色量化的顏色
colors = np.array([[0, 0, 0], [85, 85, 85], [170, 170, 170], [255, 255, 255]], dtype=np.uint8)

# 計算每個像素與 4 色量化顏色之間的距離
def quantize_color(image, colors):
    h, w, c = image.shape
    flattened_img = image.reshape(-1, 3)
    distances = np.sqrt(((flattened_img[:, None, :] - colors) ** 2).sum(axis=2))
    closest_color_indices = distances.argmin(axis=1)
    quantized_img = colors[closest_color_indices].reshape(h, w, c)
    return quantized_img

# 應用量化
quantized_image = quantize_color(image, colors)

# 有序抖動矩陣
dither_matrix = np.array([[0, 128], [192, 64]])

# 將圖片轉換為灰階並套用抖動
gray_image = cv2.cvtColor(quantized_image, cv2.COLOR_RGB2GRAY)
h, w = gray_image.shape
dithered_image = np.zeros((h, w), dtype=np.uint8)
for y in range(h):
    for x in range(w):
        threshold = dither_matrix[y % 2, x % 2]
        dithered_image[y, x] = 255 if gray_image[y, x] > threshold else 0

# 儲存結果
cv2.imshow('Output', dithered_image)
cv2.imwrite('output/output.png', dithered_image)  # 使用正確的輸出路徑
cv2.waitKey(0)
cv2.destroyAllWindows()
