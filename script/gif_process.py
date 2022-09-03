from PIL import Image,ImageSequence
import cv2
import numpy as np

import re
from pixel_transform import *

def gif_edit(path, k=16, scale=1, blur=0, erode=0, alpha = True, to_tw = False, dither=False, saturation=0, contrast=0):
    gif = Image.open(path)
    path.replace('\\', '/')
    file_name = re.split("/|\.", path)[-2]
    file_locat = path.split(file_name + '.gif')[0]

    img_list = []
    for frame in ImageSequence.Iterator(gif):
        # frame = frame.convert('RGBA')
        # opencv_img = np.array(frame, dtype=np.uint8)
        # opencv_img = cv2.cvtColor(opencv_img, cv2.COLOR_RGBA2BGRA)

        # edit area
        frame = transform(frame, k=k, scale=scale, blur=blur, erode=erode, alpha=alpha, to_tw=to_tw, dither=dither, saturation=saturation, contrast=contrast)

        img_list.append(frame)

    # output list
    output = []
    for i in img_list:
        img = i
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
        # since OpenCV is BGRA, need to change to RGBA
        img = Image.fromarray(img)
        # turn into PIL format
        img = img.convert('RGB')
        # turn into RGB ( if RGBA will turn black into alpha )
        output.append(img)
        # add to output

    # save as gif
    # output[0].save(file_locat + file_name + 'edited' + ".gif", save_all=True, append_images=output[1:], duration=200, loop=0, disposal=0)
    output[0].save(file_name + 'edited' + ".gif", save_all=True, append_images=output[1:], duration=100, loop=0, disposal=0)
    return img_list[0]

def show_gif(img_list):
    # show gif
    loop = True
    while loop:
        for i in img_list:
            cv2.imshow('gif', i)
            if cv2.waitKey(200) == ord('q'):
                loop = False
                break
    cv2.destroyAllWindows()