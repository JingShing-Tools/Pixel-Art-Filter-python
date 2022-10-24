from PIL import Image,ImageSequence
import cv2

import re
from pixel_transform import *
from tqdm import tqdm

def gif_edit(path, set_dict):
    gif = Image.open(path)

    gif_length = gif_find_length(gif)
    process = tqdm(total=gif_length)

    duration = gif.info['duration']
    path.replace('\\', '/')
    file_name = re.split("/|\.", path)[-2]
    file_locat = path.split(file_name + '.gif')[0]

    img_list = []
    for frame in ImageSequence.Iterator(gif):
        process.update(1)
        # frame = frame.convert('RGBA')
        # opencv_img = np.array(frame, dtype=np.uint8)
        # opencv_img = cv2.cvtColor(opencv_img, cv2.COLOR_RGBA2BGRA)

        # edit area
        frame = transform(frame, set_dict)
        
        cv2.imshow('frame_rendering', frame)
        if cv2.waitKey(1) == ord('q'):
            # press q to stop render
            print('Stop rendering video')
            break

        img_list.append(frame)
    cv2.destroyAllWindows()

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
    output[0].save(file_name + 'edited' + ".gif", save_all=True, append_images=output[1:], duration=duration, loop=0, disposal=0)
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

def gif_find_length(gif):
    try:
        while 1:
                gif.seek(gif.tell()+1)
                # do something to im
    except EOFError:
        pass # end of sequence
    return gif.tell()