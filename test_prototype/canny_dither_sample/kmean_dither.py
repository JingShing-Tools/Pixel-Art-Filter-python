import cv2
import numpy as np

def cv2_kmeans_quantize(image, k=8):
    h, w, c = image.shape
    image_array = image.reshape(-1, c).astype(np.float32)
    
    # 定義 KMeans 參數
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(image_array, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    quantized_array = centers[labels.flatten()]
    return quantized_array.reshape(h, w, c).astype(np.uint8)

def canny_edges(image, threshold1=100, threshold2=200):
    return cv2.Canny(image, threshold1, threshold2)

def ordered_dither(image, dither_matrix):
    h, w = image.shape[:2]
    dithered_image = np.zeros((h, w), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            threshold = dither_matrix[y % dither_matrix.shape[0], x % dither_matrix.shape[1]]
            dithered_image[y, x] = 255 if image[y, x] > threshold else 0
    return dithered_image

# 讀取和處理圖像
image = cv2.imread('image\or.jpg')
quantized_image = cv2_kmeans_quantize(image, k=4)
gray_image = cv2.cvtColor(quantized_image, cv2.COLOR_BGR2GRAY)
edges = canny_edges(gray_image)

# 應用有序抖動
dither_matrix = np.array([[0, 128], [192, 64]])  # 2x2抖動矩陣
smooth_dithered_image = ordered_dither(edges, dither_matrix)

# 顯示結果
cv2.imshow('Quantized Image', quantized_image)
# cv2.imshow('Edges', edges)
# cv2.imshow('Smooth Dithered Image', smooth_dithered_image)
cv2.imwrite('image\or_test.jpg', quantized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
