from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import re
from pixel_converter import *
from settings import resource_path, sample_image_path

class Gui_helper:
    def __init__(self, display):
        self.display = display
        self.root= Tk()
        self.root.iconbitmap(resource_path('assets/icon/icon.ico'))

        self.image_path = resource_path(sample_image_path)
        self.cv_image = cv2.imread(self.image_path)

        self.root.title('pixel art styler像素風格濾鏡工具')
        self.root.geometry('500x300')

        self.load_file_name = StringVar()
        self.load_file_name.set('no file無檔案')
        self.now_file_name = Label(self.root,textvariable=self.load_file_name)
        self.now_file_name.grid(column=0, row=0, sticky=N+W)

        self.import_img_btn = Button(self.root, text='import img導入圖片', command=self.import_img)
        self.import_img_btn.grid(column=4, row=0, sticky=E+N)

        # color num
        self.color_num_name = Label(self.root,text='Color nums色數')
        self.color_num_name.grid(column=0, row=1, sticky=N+W)
        self.color_num_select_box = Combobox(self.root, width=5)
        self.color_num_select_box.grid(column=0, row=2, sticky=N+W)
        self.color_num_select_box['values'] = ['2', '4', '8', '16','32','64', '128']
        self.color_num_select_box.current(0)
        # pixel size
        self.pixel_size_name = Label(self.root,text='Pixel size像素尺寸')
        self.pixel_size_name.grid(column=4, row=1, sticky=N+E)
        self.pixel_size_select_box = Combobox(self.root, width=5)
        self.pixel_size_select_box.grid(column=4, row=2, sticky=N+E)
        self.pixel_size_select_box['values'] = ['1', '2', '3', '4']
        self.pixel_size_select_box.current(0)
        # smoothing
        self.smoothing_name = Label(self.root,text='Smoothing光滑')
        self.smoothing_name.grid(column=0, row=3, sticky=N+W)
        self.smoothing_select_box = Combobox(self.root, width=5)
        self.smoothing_select_box.grid(column=0, row=4, sticky=N+W)
        self.smoothing_select_box['values'] = ['None', 'Less', 'Great']
        self.smoothing_select_box.current(0)
        # outlines
        self.outline_name = Label(self.root,text='Outline輪廓')
        self.outline_name.grid(column=4, row=3, sticky=N+E)
        self.outline_select_box = Combobox(self.root, width=5)
        self.outline_select_box.grid(column=4, row=4, sticky=N+E)
        self.outline_select_box['values'] = ['None', 'Less', 'Great']
        self.outline_select_box.current(0)
        # saturation
        self.saturation_name = Label(self.root,text='Saturation飽和')
        self.saturation_name.grid(column=0, row=5, sticky=N+W)
        self.saturation_select_box = Combobox(self.root, width=5)
        self.saturation_select_box.grid(column=0, row=6, sticky=N+W)
        self.saturation_select_box['values'] = ['-200', '-150', '-100', '-50', '0', '50', '100', '150', '200']
        self.saturation_select_box.current(2)
        # contrast
        self.contrast_name = Label(self.root,text='Contrast對比')
        self.contrast_name.grid(column=4, row=5, sticky=N+E)
        self.contrast_select_box = Combobox(self.root, width=5)
        self.contrast_select_box.grid(column=4, row=6, sticky=N+E)
        self.contrast_select_box['values'] = ['-200', '-150', '-100', '-50', '0', '50', '100', '150', '200']
        self.contrast_select_box.current(2)

        # dithering
        self.dithering_bool = BooleanVar()
        self.dithering_check = Checkbutton(self.root, text='Dithering顆粒抖動', variable=self.dithering_bool)
        self.dithering_check.grid(column=0, row=7, sticky=N+W)
        
        # transform button
        self.transform_img_btn = Button(self.root, text='transform變換', command=self.transform_img)
        self.transform_img_btn.grid(column=0, row=8, sticky=W+N)
        # save_img button
        self.save_img_btn = Button(self.root, text='save保存', command=self.save_img)
        self.save_img_btn.grid(column=0, row=9, sticky=W+N)

    def import_img(self):
        image_path = filedialog.askopenfilename()
        if image_path:
            file_name = re.split('/|\.', image_path)[-2]
            # print(image_path)
            self.load_file_name.set(file_name)
            self.display.image_load(image_path)
            self.image_path = image_path
            self.cv_image = cv2.imread(self.image_path)

    def transform_img(self):
        k = int(self.color_num_select_box.get())
        scale = int(self.pixel_size_select_box.get())
        blur = self.get_textbox_value(self.smoothing_select_box.get())
        erode = self.get_textbox_value(self.outline_select_box.get())
        dither = self.dithering_bool.get()
        saturation = int(self.saturation_select_box.get())
        contrast = int(self.contrast_select_box.get())

        self.cv_image = convert(self.image_path, 
                                k=k, 
                                scale=scale, 
                                blur=blur, 
                                erode=erode, 
                                dither=dither, 
                                saturation=saturation, 
                                contrast=contrast)
        self.display.cv_to_pygame(self.cv_image)

    def get_textbox_value(self, text):
        if text == 'None':
            return 0
        elif text == 'Less':
            return 1
        elif text == 'Great':
            return 2

    def save_img(self):
        save_cv_img(self.cv_image, './', self.load_file_name.get() + '_pixel')

    def run(self):
        self.root.mainloop()