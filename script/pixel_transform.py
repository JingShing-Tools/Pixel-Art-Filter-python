import cv2
from PIL import Image
import numpy as np
from bayer_dithering import *
from contrast_and_saturation import contrast_and_brightness, saturation_and_lightness
from settings import pixel_set_dict_to_all_sets

n8 = np.ones((3, 3), np.uint8)
n4 = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], np.uint8)

def transform(src, set_dict):
    k, scale, color, blur, erode, alpha, to_tw, dither, saturation, contrast = pixel_set_dict_to_all_sets(set_dict)
    
    # 判斷 src 類型並加載圖片
    img, alpha_mode = load_image(src, alpha)
    
    # 色彩處理
    img = process_color(img, color, alpha_mode)
    h, w = img.shape[:2]
    d_h, d_w = int(h / scale), int(w / scale)

    # 圖像處理：腐蝕、模糊和縮放
    img = apply_filters(img, erode, blur, d_w, d_h)

    # 飽和度和對比度調整
    img = apply_saturation_contrast(img, saturation, contrast)

    # K-means 色彩量化
    img = apply_kmeans(img, k, color, d_w, d_h, scale, alpha_mode, to_tw)

    # 抖動處理
    if dither:
        img = dither_color_image_by_dither_map(img, bayerMatrix_8X8_1)
    
    return img

def load_image(src, alpha):
    if isinstance(src, np.ndarray):
        return src, False

    img = Image.open(src) if isinstance(src, str) else src
    alpha_mode = (img.mode in ('RGBA', 'P') and alpha)
    
    if alpha_mode:
        img = img.convert('RGBA') if img.mode != 'RGBA' else img
    elif img.mode not in ('RGB', 'L'):
        img = img.convert('RGB')
        
    return np.asarray(img), alpha_mode

def process_color(img, color, alpha_mode):
    if color and alpha_mode:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
    elif color:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return img

def apply_filters(img, erode, blur, d_w, d_h):
    if erode:
        kernel = n4 if erode == 1 else n8
        img = cv2.erode(img, kernel, iterations=1)
    if blur:
        img = cv2.bilateralFilter(img, 15, blur, 20)
    return cv2.resize(img, (d_w, d_h), interpolation=cv2.INTER_NEAREST)

def apply_saturation_contrast(img, saturation, contrast):
    if saturation != 0:
        img = saturation_and_lightness(img, lightness=0, saturation=saturation)
    if contrast != 0:
        img = contrast_and_brightness(img, brightness=0, contrast=contrast)
    return img

def apply_kmeans(img, k, color, d_w, d_h, scale, alpha_mode, to_tw):
    img_cp = img.reshape(-1, img.shape[2] if color else 1).astype(np.float32)
    _, label, center = cv2.kmeans(img_cp, k, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0), 10, cv2.KMEANS_PP_CENTERS)
    center = center.astype(np.uint8)
    result = center[label.flatten()].reshape(img.shape)
    result = cv2.resize(result, (d_w * scale, d_h * scale), interpolation=cv2.INTER_NEAREST)
    
    if alpha_mode:
        result = add_alpha_channel(result, img, d_w, d_h, scale)
    elif to_tw:
        result = add_transparency_channel(result)
        
    return result

def add_alpha_channel(result, img, d_w, d_h, scale):
    alpha_channel = cv2.resize(img[:, :, 3], (d_w, d_h), interpolation=cv2.INTER_NEAREST)
    alpha_channel = cv2.resize(alpha_channel, (d_w * scale, d_h * scale), interpolation=cv2.INTER_NEAREST)
    alpha_channel[alpha_channel != 0] = 255
    if not 0 in alpha_channel:
        alpha_channel[0, 0] = 0
    return cv2.merge((*cv2.split(result), alpha_channel))

def add_transparency_channel(result):
    r, g, b = cv2.split(result)
    alpha_channel = np.ones(r.shape, dtype=np.uint8) * 255
    alpha_channel[0, 0] = 0
    return cv2.merge((r, g, b, alpha_channel))

def get_color(center):
    colors = ['#{:02x}{:02x}{:02x}'.format(*map(int, c[::-1])) for c in center]
    print(colors)
    return colors