import os
import re
import cv2
from pixel_transform import transform
from settings import resource_path

def convert(img_path, k=16, scale=1, blur=0, erode=0,alpha = True, to_tw = False, dither=False):
    # k is color num
    # scale is pixel size
    # to_tw means to twitter
    img_path.replace("\\", "/")
    img_file_name = re.split("/", img_path)[-1]
    img_res = transform(img_path, k=k, scale=scale, blur=blur, erode=erode, alpha=alpha, to_tw=to_tw, dither=dither)
    img_path = img_path.split(img_file_name)[0]
    return img_res

def save_cv_img(img, img_path, img_name):
    result_path = os.path.join(img_path + img_name + '.png')
    cv2.imwrite(result_path, img, [int(cv2.IMWRITE_PNG_COMPRESSION)])