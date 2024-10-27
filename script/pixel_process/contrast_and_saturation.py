import cv2
import numpy as np
import math

def contrast_and_brightness(img, brightness=0, contrast=100):
    B = brightness / 255.0
    c = contrast / 255.0
    k = math.tan((45 + 44 * c) / 180 * math.pi)

    adjusted_img = (img - 127.5 * (1 - B)) * k + 127.5 * (1 + B)
    return np.clip(adjusted_img, 0, 255).astype(np.uint8)

def saturation_and_lightness(img, lightness, saturation):
    fImg = img.astype(np.float32) / 255.0
    hlsImg = cv2.cvtColor(fImg, cv2.COLOR_BGR2HLS)

    # 調整亮度和飽和度
    hlsImg[:, :, 1] = np.clip(hlsImg[:, :, 1] * (1 + lightness / 100.0), 0, 1)
    hlsImg[:, :, 2] = np.clip(hlsImg[:, :, 2] * (1 + saturation / 100.0), 0, 1)

    result_img = (cv2.cvtColor(hlsImg, cv2.COLOR_HLS2BGR) * 255).astype(np.uint8)
    return result_img
