import os
import sys

sample_image_path = "assets/image/1.png"

def resource_path(relative):
    """Returns the absolute path for resource files, adjusting for bundled environments."""
    return os.path.join(getattr(sys, "_MEIPASS", ""), relative)

def pixel_set_to_dict(k=2, scale=4, color=True, blur=0, erode=0, alpha=True, to_tw=False, dither=False, saturation=0, contrast=0):
    """Creates a dictionary with pixel transformation settings."""
    return {
        'bit': k,
        'pixel_size': scale,
        'color': color,
        'blur': blur,
        'erode': erode,
        'alpha': alpha,
        'to_tw': to_tw,
        'dither': dither,
        'saturation': saturation,
        'contrast': contrast,
    }

def pixel_set_dict_to_all_sets(pixel_set_dict):
    """Extracts pixel transformation settings from a dictionary."""
    return (
        pixel_set_dict['bit'],
        pixel_set_dict['pixel_size'],
        pixel_set_dict['color'],
        pixel_set_dict['blur'],
        pixel_set_dict['erode'],
        pixel_set_dict['alpha'],
        pixel_set_dict['to_tw'],
        pixel_set_dict['dither'],
        pixel_set_dict['saturation'],
        pixel_set_dict['contrast'],
    )
