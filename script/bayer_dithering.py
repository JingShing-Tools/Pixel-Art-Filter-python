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

def detect_board_color(img, y, x, allow_value, mode, select_color_value=None):
    # mode : 0, 8 dir. 1, 4 dir.
    # allow_value
    # select_color_value should be tuple
    height = img.shape[0]
    width = img.shape[1]
    self_color = img[y][x]
    tel = False
    dir = None
    if select_color_value:
        if self_color >= select_color_value[0] and self_color <= select_color_value[1]:
            pass
        else:
            return tel, dir
    if mode == 0:
        x_dir = [1, 1, 1, 1, -1, -1, -1, -1]
        y_dir = [1, -1, 1, -1, 1, -1, 1, -1]
        for i in range(8):
            new_y = y + y_dir[i]
            new_x = x + x_dir[i]
            new_y = clamp(new_y, height-1, 0)
            new_x = clamp(new_x, width-1, 0)
            new_color = img[new_y][new_x]
            if self_color >= new_color+allow_value or self_color <= new_color-allow_value:
                if select_color_value:
                    if new_color >= select_color_value[0] and new_color <= select_color_value[1]:
                        # new color in select_color_value range
                        return True, i
                    else:
                        continue
                else:
                    return True, i
        return tel, dir
    elif mode == 1:
        x_dir = [1, 1, -1, -1]
        y_dir = [1, -1, 1, -1]
        for i in range(4):
            new_y = y + y_dir[i]
            new_x = x + x_dir[i]
            new_y = clamp(new_y, height-1, 0)
            new_x = clamp(new_x, width-1, 0)
            new_color = img[new_y][new_x]
            if self_color >= new_color+allow_value or self_color <= new_color-allow_value:
                return True, i
        return tel, dir
        
def clamp(value, max_num, min_num):
    value = max(value, min_num)
    value = min(value, max_num)
    # value = value % max_num
    return value

def process_dither_color_fixed_8_dir(img, matrix, allow_value, mode, select_color_value):
    or_img = img.copy()
    height = img.shape[0]
    width = img.shape[1]
    matrix_len = len(matrix) - 1
    for row in range(height):
        for col in range(width):
            tel, dir = detect_board_color(or_img, row, col, allow_value, mode, select_color_value)
            if tel:
                color = img[row][col]
                
                if color >= (color>>2) > matrix[row&matrix_len][col&matrix_len]:
                    v = 255
                else:
                    v = 0

                img[row][col] = v

def dither_color_image_fix(image, matrix, allow_value, mode, select_color_value=None):
    blue=image[:,:,0]  #taking the blue channel
    process_dither_color_fixed_8_dir(blue, matrix, allow_value, mode, select_color_value)
    green=image[:,:,1]
    process_dither_color_fixed_8_dir(green, matrix, allow_value, mode, select_color_value)
    red=image[:,:,2]
    process_dither_color_fixed_8_dir(red, matrix, allow_value, mode, select_color_value)
    return cv2.merge((blue, green, red))

def get_dither_map_dir(img, allow_value=30, mode=0, select_color_value=None):
    or_img = img.copy()
    height = img.shape[0]
    width = img.shape[1]
    dither_map = []
    for row in range(height):
        for col in range(width):
            tel, dir = detect_board_color(or_img, row, col, allow_value, mode, select_color_value)
            if tel:
                # color = img[row][col]
                dither_map.append((row, col, dir))
    return dither_map                

def get_dither_map_by_gray(image, allow_value=40, mode=0, select_color_value=None):
    # mode 0 is best. mode 1 is fast
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return get_dither_map_dir(gray_img, allow_value, mode, select_color_value=select_color_value)

def use_dither_map_to_dither(img, matrix, dither_map):
    height = img.shape[0]
    width = img.shape[1]
    x_dir = [1, 1, 1, 1, -1, -1, -1, -1]
    y_dir = [1, -1, 1, -1, 1, -1, 1, -1]
    matrix_len = len(matrix) - 1
    for pos in dither_map:
        color = img[pos[0]][pos[1]]
        if color >= (color>>2) > matrix[pos[0]&matrix_len][pos[1]&matrix_len]:
            img[pos[0]][pos[1]] = img[clamp(pos[0]+y_dir[pos[2]], height-1, 0)][clamp(pos[1]+x_dir[pos[2]], width-1, 0)]
        else:
            pass

def dither_color_image_by_dither_map(image, matrix):
    # dither_map = get_dither_map_by_gray(image, 30, 0, (0, 100))
    dither_map = get_dither_map_by_gray(image, 30, 0, (20, 100))
    blue=image[:,:,0]  #taking the blue channel
    use_dither_map_to_dither(blue, matrix, dither_map)
    green=image[:,:,1]
    use_dither_map_to_dither(green, matrix, dither_map)
    red=image[:,:,2]
    use_dither_map_to_dither(red, matrix, dither_map)
    return cv2.merge((blue, green, red))
