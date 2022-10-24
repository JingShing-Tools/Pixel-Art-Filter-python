import cv2
from PIL import Image
import numpy as np
from bayer_dithering import *
from contrast_and_saturation import contrast_and_brightness, saturation_and_lightness
from settings import pixel_set_dict_to_all_sets

n8 = np.array([[1, 1, 1],
               [1, 1, 1],
               [1, 1, 1]],
              np.uint8)

n4 = np.array([[0, 1, 0],
               [1, 1, 1],
               [0, 1, 0]],
              np.uint8)

def transform(src, set_dict):
    k, scale, color, blur, erode, alpha, to_tw, dither, saturation, contrast = pixel_set_dict_to_all_sets(set_dict)
    # if src is string means it's a path
    # else it is PIL image
    if type(src).__name__ == 'ndarray':
        alpha_mode = False
        img = src
    else:
        if type(src).__name__=='str':
            img_pl = Image.open(src)
        elif type(src).__name__=='JpegImageFile':
            img_pl = src
        elif type(src).__name__=='GifImageFile':
            img_pl = src
        else:
            img_pl = src

        if (img_pl.mode == 'RGBA' or img_pl.mode == 'P') and alpha:
            if img_pl.mode != 'RGBA':
                img_pl = img_pl.convert('RGBA')
            alpha_mode = True
        elif img_pl.mode != 'RGB' and img_pl.mode != 'L':
            img_pl = img_pl.convert('RGB')
            alpha_mode = False
        else:
            alpha_mode = False
            
        img = np.asarray(img_pl)

    if color and alpha_mode:
        a = img[:, :, 3]
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        h, w, c = img.shape
    elif color:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, c = img.shape
    else:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        h, w = img.shape
        c = 0
    d_h = int(h / scale)
    d_w = int(w / scale)
    if erode == 1:
        img = cv2.erode(img, n4, iterations=1)
    elif erode == 2:
        img = cv2.erode(img, n8, iterations=1)
    if blur:
        img = cv2.bilateralFilter(img, 15, blur, 20)

    img = cv2.resize(img, (d_w, d_h), interpolation=cv2.INTER_NEAREST)

    if saturation != 0:
        img = saturation_and_lightness(img, lightness=0, saturation=saturation)
    if contrast != 0:
        img = contrast_and_brightness(img, brightness=0, contrast=contrast)

    if dither:
        img = dither_color_image_by_dither_map(img, bayerMatrix_8X8_1)
        # cv2.imshow('img', img)
        # img = dither_color_image(img, bayerMatrix_8X8_1)

    if alpha_mode:
        a = cv2.resize(a, (d_w, d_h), interpolation=cv2.INTER_NEAREST)
        a = cv2.resize(a, (d_w * scale, d_h * scale), interpolation=cv2.INTER_NEAREST)
        a[a != 0] = 255
        if not 0 in a:
            a[0, 0] = 0
    if color:
        img_cp = img.reshape(-1, c)
    else:
        img_cp = img.reshape(-1)
    img_cp = img_cp.astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(img_cp, k, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
    center = center.astype(np.uint8)
    result = center[label.flatten()]
    result = result.reshape((img.shape))
    result = cv2.resize(result, (d_w * scale, d_h * scale), interpolation=cv2.INTER_NEAREST)
    if alpha_mode:
        r, g, b = cv2.split(result)
        result = cv2.merge((r, g, b, a))
    elif to_tw:
        r, g, b = cv2.split(result)
        a = np.ones(r.shape, dtype=np.uint8) * 255
        a[0, 0] = 0
        result = cv2.merge((r, g, b, a))
    # colors = get_color(center)

    return result

def get_color(center):
    # get colors
    colors = []
    for res_c in center:
        color_code = '#{0:02x}{1:02x}{2:02x}'.format(res_c[2], res_c[1], res_c[0])
        colors.append(color_code)
    print(colors)
    return colors