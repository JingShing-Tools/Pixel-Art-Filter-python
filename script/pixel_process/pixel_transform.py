import cv2
from PIL import Image
import numpy as np
from pixel_process.bayer_dithering import *
from pixel_process.contrast_and_saturation import contrast_and_brightness, saturation_and_lightness
from settings import pixel_set_dict_to_all_sets

n8 = np.ones((3, 3), np.uint8)
n4 = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], np.uint8)

def transform(src, set_dict):
    k, scale, color, blur, erode, alpha, dither, saturation, contrast = pixel_set_dict_to_all_sets(set_dict)
    
    # 判斷 src 類型並加載圖片
    img, alpha_mode = load_image(src, alpha)
    
    # 色彩處理
    img = process_color(img, color, alpha_mode)
    h, w = img.shape[:2]
    d_h, d_w = int(h / scale), int(w / scale)

    # 去除雜點
    img = remove_noise(img)

    # 圖像處理：腐蝕、模糊和縮放
    img = apply_filters(img, erode, blur)
    img = resize_to_small_size(img, d_w, d_h)

    # 飽和度和對比度調整
    img = apply_saturation_contrast(img, saturation, contrast)

    # K-means 色彩量化
    img, colors = apply_kmeans(img, k, color, d_w, d_h, scale, alpha_mode)
    img = resize_to_original_size(img, d_w, d_h, scale)

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

def remove_noise(img):
    # 使用中值濾波去除小噪點
    img = cv2.medianBlur(img, 3)  # 可調整 kernel size 為 3 或 5

    # 使用開運算去除噪點
    kernel = np.ones((3, 3), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    
    return img

def process_color(img, color, alpha_mode):
    if color and alpha_mode:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
    elif color:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return img

def apply_filters(img, erode, blur):
    if erode:
        kernel = n4 if erode == 1 else n8
        img = cv2.erode(img, kernel, iterations=1)
    if blur:
        img = cv2.bilateralFilter(img, 15, blur, 20)
    return img

def apply_saturation_contrast(img, saturation, contrast):
    if saturation != 0:
        img = saturation_and_lightness(img, lightness=0, saturation=saturation)
    if contrast != 0:
        img = contrast_and_brightness(img, brightness=0, contrast=contrast)
    return img

def apply_kmeans(img, k, color, d_w, d_h, scale, alpha_mode, palette=None):
    img_cp = img.reshape(-1, img.shape[2] if color else 1).astype(np.float32)

    if palette is not None:
        palette = [color if color.startswith('#') else f'#{color}' for color in palette]        
        palette = np.array([[int(color[i:i+2], 16) for i in (5, 3, 1)] for color in palette], dtype=np.float32)
        k = len(palette)
        img_cp = img.reshape(-1, img.shape[2] if color else 1).astype(np.float32)        
        label = np.argmin(np.linalg.norm(img_cp[:, None] - palette, axis=2), axis=1)
        center = palette
    else:
        _, label, center = cv2.kmeans(img_cp, k, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0), 10, cv2.KMEANS_PP_CENTERS)
    center = center.astype(np.uint8)
    result = center[label.flatten()].reshape(img.shape)
    
    if alpha_mode:
        result = add_alpha_channel(result, img, d_w, d_h, scale)

    colors = get_color(center)
        
    return result, colors

def resize_to_small_size(img, d_w, d_h):
    return cv2.resize(img, (d_w, d_h), interpolation=cv2.INTER_NEAREST)

def resize_to_original_size(img, d_w, d_h, scale):
    return cv2.resize(img, (d_w * scale, d_h * scale), interpolation=cv2.INTER_NEAREST)

def add_alpha_channel(result, img, d_w, d_h, scale):
    # 檢查圖像是否有 alpha 通道
    if img.shape[2] == 4:
        # 調整 alpha 通道大小
        alpha_channel = cv2.resize(img[:, :, 3], (d_w, d_h), interpolation=cv2.INTER_NEAREST)
        alpha_channel = cv2.resize(alpha_channel, (d_w * scale, d_h * scale), interpolation=cv2.INTER_NEAREST)
        alpha_channel[alpha_channel != 0] = 255
        
        # 確保至少有一個像素的 alpha 值為 0
        if not 0 in alpha_channel:
            alpha_channel[0, 0] = 0
        
        # 將 alpha 通道合併到結果圖像
        return cv2.merge((*cv2.split(result), alpha_channel))
    else:
        # 如果沒有 alpha 通道，直接返回原始 result
        print("Warning: No alpha channel found in image. Skipping alpha channel processing.")
        return result

def get_color(center):
    colors = ['#{:02x}{:02x}{:02x}'.format(*map(int, c[::-1])) for c in center]
    print(colors)
    print(len(colors))
    return colors