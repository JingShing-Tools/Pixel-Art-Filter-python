import os
import re
import cv2
from pixel_transform import transform
from gif_process import gif_edit
from video_editor import video_edit

def convert(img_path, set_dict):
    # k is color num
    # scale is pixel size
    # to_tw means to twitter
    img_path.replace("\\", "/")
    img_file_name = re.split("/", img_path)[-1]
    img_file_format = img_file_name.split('.')[-1]
    if img_file_format in ['gif', 'GIF']:
        img_res = gif_edit(img_path, set_dict)
    elif img_file_format in ['mp4', 'avi', 'flv']:
        img_res = video_edit(img_path, set_dict)
    else:
        img_res = transform(img_path, set_dict)
        img_path = img_path.split(img_file_name)[0]
    # cv2.imshow('show', img_res)
    return img_res

def save_cv_img(img, img_path, img_name):
    result_path = os.path.join(img_path + img_name + '.png')
    cv2.imwrite(result_path, img, [cv2.IMWRITE_PNG_COMPRESSION, 9])