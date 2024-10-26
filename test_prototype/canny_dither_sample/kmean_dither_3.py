import cv2
import numpy as np

def cv2_kmeans_quantize(image, k=8):
    h, w, c = image.shape
    image_array = image.reshape(-1, c).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(image_array, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    quantized_array = centers[labels.flatten()]
    return quantized_array.reshape(h, w, c).astype(np.uint8)

def canny_edges(image, threshold1=100, threshold2=200):
    return cv2.Canny(image, threshold1, threshold2)

def ordered_dither_color(edges, image, dither_matrix):
    h, w, c = image.shape
    dithered_image = image.copy()
    # 擴大或淡化邊緣
    edges_blurred = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)
    for i in range(c):
        for y in range(h):
            for x in range(w):
                if edges_blurred[y, x] > 0:  # 只在邊緣範圍內進行抖動
                    threshold = dither_matrix[y % dither_matrix.shape[0], x % dither_matrix.shape[1]]
                    dithered_image[y, x, i] = 255 if image[y, x, i] > threshold else 0
    return dithered_image


# 讀取和處理圖像
image = cv2.imread('test_prototype/canny_dither_sample/image/or.jpg')
quantized_image = cv2_kmeans_quantize(image, k=8)
gray_image = cv2.cvtColor(quantized_image, cv2.COLOR_BGR2GRAY)
edges = canny_edges(gray_image)

# 應用有序抖動
dither_matrix = np.array([[0, 128], [192, 64]])  # 2x2抖動矩陣
smooth_dithered_image = ordered_dither_color(edges, quantized_image, dither_matrix)

# 顯示結果
cv2.imshow('Quantized Image', quantized_image)
cv2.imshow('Edges', edges)
cv2.imshow('Smooth Dithered Image', smooth_dithered_image)
cv2.imwrite('test_prototype/canny_dither_sample/image/or_test.jpg', smooth_dithered_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
