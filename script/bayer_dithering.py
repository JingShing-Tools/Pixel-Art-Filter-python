import cv2

bayerMatrix_8X8_1 = [
                [0,48,12,60,3,51,15,63],
                [32,16,44,28,35,19,47,31],
                [8,56,4,52,11,59,7,55],
                [40,24,36,20,43,27,39,23],
                [2,50,14,62,1,49,13,61],
                [34,18,46,30,33,17,45,29],
                [10,58,6,54,9,57,5,53],
                [42,26,38,22,41,25,37,21]
            ]

bayerMatrix_8X8_2 = [
    [ 0, 32, 8, 40, 2, 34, 10, 42], ### 8x8 Bayer ordered dithering 
    [48, 16, 56, 24, 50, 18, 58, 26], ### pattern. Each input pixel 
    [12, 44, 4, 36, 14, 46, 6, 38], ### is scaled to the 0..63 range 
    [60, 28, 52, 20, 62, 30, 54, 22], ### before looking in this table 
    [ 3, 35, 11, 43, 1, 33, 9, 41], ### to determine the action. 
    [51, 19, 59, 27, 49, 17, 57, 25],
    [15, 47, 7, 39, 13, 45, 5, 37],
    [63, 31, 55, 23, 61, 29, 53, 21] 
]

bayerMatrix_4X4_1 = [
    [0, 8, 2, 10],
    [12, 4, 14, 6],
    [3, 11, 1, 9],
    [15, 7, 13, 5],
]

bayerMatrix_3X3_1 = [
    [0, 7, 3],
    [6, 5, 2],
    [4, 1, 8],
]

bayerMatrix_2X2_1 = [
    [0, 2],
    [3, 1],
]

def process_dither_color(img, matrix):
    height = img.shape[0]
    width = img.shape[1]
    matrix_len = len(matrix) - 1
    for row in range(height):
        for col in range(width):

            color = img[row][col]
            
            if color >= (color>>2) > matrix[row&matrix_len][col&matrix_len]:
                v = 255
            else:
                v = 0

            img[row][col] = v    

def dither_color_image(image, matrix):
    blue=image[:,:,0]  #taking the blue channel
    process_dither_color(blue, matrix)
    green=image[:,:,1]
    process_dither_color(green, matrix)
    red=image[:,:,2]
    process_dither_color(red, matrix)
    return cv2.merge((blue, green, red))