import cv2
import numpy
import math

def contrast_and_brightness(img, brightness=0 , contrast=100):
    B = brightness / 255.0
    c = contrast / 255.0 
    k = math.tan((45 + 44 * c) / 180 * math.pi)

    img = (img - 127.5 * (1 - B)) * k + 127.5 * (1 + B)
      
    # values between 0-255
    img = numpy.clip(img, 0, 255).astype(numpy.uint8)
    return img
    
def saturation_and_lightness(img, lightness, saturation):
    # origin_img = img

    # astype image and turn to float
    fImg = img.astype(numpy.float32)
    fImg = fImg / 255.0

    # color space exchange BGR -> HLS
    hlsImg = cv2.cvtColor(fImg, cv2.COLOR_BGR2HLS)
    hlsCopy = numpy.copy(hlsImg)

    # lightness = 0 # lightness edited to "1 +/- n %"
    # saturation = 300 # saturation edited to "1 +/- n %"

    # brightness
    hlsCopy[:, :, 1] = (1 + lightness / 100.0) * hlsCopy[:, :, 1]
    hlsCopy[:, :, 1][hlsCopy[:, :, 1] > 1] = 1  # Between 0-1

    # saturation
    hlsCopy[:, :, 2] = (1 + saturation / 100.0) * hlsCopy[:, :, 2]
    hlsCopy[:, :, 2][hlsCopy[:, :, 2] > 1] = 1  # Between 0-1

    # color space exchange back HLS -> BGR 
    result_img = cv2.cvtColor(hlsCopy, cv2.COLOR_HLS2BGR)
    result_img = ((result_img * 255).astype(numpy.uint8))
    return result_img