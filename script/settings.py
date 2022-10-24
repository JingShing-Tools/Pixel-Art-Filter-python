import os, sys

sample_image_path = "assets/image/1.png"

def resource_path(relative):
	if hasattr(sys, "_MEIPASS"):
		absolute_path = os.path.join(sys._MEIPASS, relative)
	else:
		absolute_path = os.path.join(relative)
	return absolute_path

def pixel_set_to_dict(k=2, scale=4, color=True, blur=0, erode=0, alpha=True, to_tw=False, dither=False, saturation=0, contrast=0):
	pixel_set_dict = {}
	pixel_set_dict['bit'] = k
	pixel_set_dict['pixel_size'] = scale
	pixel_set_dict['color'] = color
	pixel_set_dict['blur'] = blur
	pixel_set_dict['erode'] = erode
	pixel_set_dict['alpha'] = alpha
	pixel_set_dict['to_tw'] = to_tw
	pixel_set_dict['dither'] = dither
	pixel_set_dict['saturtion'] = saturation
	pixel_set_dict['contrast'] = contrast
	return pixel_set_dict

def pixel_set_dict_to_all_sets(pixel_set_dict):
	k = pixel_set_dict['bit']
	scale = pixel_set_dict['pixel_size']
	color = pixel_set_dict['color']
	blur = pixel_set_dict['blur']
	erode = pixel_set_dict['erode'] 
	alpha = pixel_set_dict['alpha'] 
	to_tw = pixel_set_dict['to_tw'] 
	dither = pixel_set_dict['dither']
	saturation = pixel_set_dict['saturtion']
	contrast = pixel_set_dict['contrast']
	return k, scale, color, blur, erode, alpha, to_tw, dither, saturation, contrast

# pixel_set_dict['bit']
# pixel_set_dict['pixel_size']
# pixel_set_dict['color']
# pixel_set_dict['blur']
# pixel_set_dict['erode'] 
# pixel_set_dict['alpha'] 
# pixel_set_dict['to_tw'] 
# pixel_set_dict['dither']
# pixel_set_dict['saturtion']
# pixel_set_dict['contrast'] 