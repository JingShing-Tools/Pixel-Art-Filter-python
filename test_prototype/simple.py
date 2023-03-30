import cv2
from PIL import Image
import numpy as np

def transform(src, k, scale, blur):
    img_pl = Image.open(src)
    img = np.asarray(img_pl)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, c = img.shape
    d_h = int(h / scale)
    d_w = int(w / scale)
    if blur:
        img = cv2.bilateralFilter(img, 15, blur, 20)

    img = cv2.resize(img, (d_w, d_h), interpolation=cv2.INTER_NEAREST)
    img_cp = img.reshape(-1, c)
    img_cp = img_cp.astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(img_cp, k, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
    center = center.astype(np.uint8)
    result = center[label.flatten()]
    result = result.reshape((img.shape))
    result = cv2.resize(result, (d_w * scale, d_h * scale), interpolation=cv2.INTER_NEAREST)

    return result

def save_cv_img(img, img_name):
    cv2.imwrite(img_name, img, [cv2.IMWRITE_PNG_COMPRESSION, 9])

if __name__ == "__main__":
    file = "image/or.jpg"
    save_cv_img(transform(file, 3, 1, 0), "test_py.png")
