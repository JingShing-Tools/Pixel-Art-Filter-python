from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import re
from pixel_converter import *
from settings import resource_path, sample_image_path
from tkinter import messagebox

def clamp(value, max_num, min_num):
    value = max(value, min_num)
    value = min(value, max_num)
    # value = value % max_num
    return value

# don't use Tk to initialize your class in threading
class Gui_helper_main:
    def __init__(self, display):
        self.root = Tk()
        self.frame = None
        self.frame_index = 0
        self.display = display
        self.root.iconbitmap(resource_path('assets/icon/icon.ico'))
        self.root.geometry('500x300')
        self.root.title('pixel art styler像素風格濾鏡工具')
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        # maker info
        self.maker_name = Label(self.root, text="Maker : JingShing季旬")
        self.maker_name.grid(column=0, row=3, sticky=N+W)
        
        # mode hint
        self.mode_now = StringVar()
        self.mode_now.set("Mode: Simple")
        self.maker_name = Label(self.root, textvariable=self.mode_now)
        self.maker_name.grid(column=0, row=2, sticky=N+W)

        self.load_file_name = StringVar()
        self.load_file_name.set('no file無檔案')
        self.image_path = resource_path(sample_image_path)
        self.cv_image = cv2.imread(self.image_path)

        # A rule to only input digits
        self.only_digit_vcmd = (self.root.register(self.only_digit), '%P')

        self.frames = [Gui_helper_simple_page(self), Gui_helper_custom_page(self)]
        self.switch_frame(0)
        
    def only_digit(self, input_str):
        if input_str == '':
            return True
        elif input_str[0] == '+' or input_str[0] == '-' or str.isdigit(input_str[0]):
            str_len = len(input_str)
            cmp_str = input_str[1:str_len]
            # print(cmp_str)
            if str.isdigit(cmp_str) or cmp_str == '':
                return True
            else:
                return False
        # elif str.isdigit(input_str) or input_str == '':
        #     return True
        else:
            return False

    def switch_frame(self, index):
        # new_frame = frame_class(self)
        # if self.frame is not None:
        #     self.frame.destroy()
        #     del self.frame
        #     self.frame.kill()
        if self.frame is not None:
            self.frame.grid_forget()
        self.frame_index = index
        self.frame = self.frames[self.frame_index]
        self.mode_now.set("Mode: " + self.frame.mode)
        self.frame.grid(column=0, row=0, sticky=N+W)

    def run(self):
        self.root.mainloop()

    def quit(self):
        if messagebox.askyesno('Confirm','Are you sure you want to quit?'):
            #In order to use quit function, mainWindow MUST BE an attribute of Interface.
            # self.root.destroy()
            self.root.quit()
            # del self

class Gui_helper_page_module(Frame):
    def __init__(self, master):
        Frame.__init__(self, master = master.root)
        self.main = master
        self.master = master.root

    def custom_mode_switch(self):
        self.main.switch_frame(1)

    def simple_mode_switch(self):
        self.main.switch_frame(0)

    def import_img(self):
        image_path = filedialog.askopenfilename()
        if image_path:
            file_name = re.split('/|\.', image_path)[-2]
            # print(image_path)
            self.main.load_file_name.set(file_name)
            self.main.display.image_load(image_path)
            self.main.image_path = image_path
            self.main.cv_image = cv2.imread(self.main.image_path)

    def transform_img(self):
        k = int(self.color_num_select_box.get())
        scale = int(self.pixel_size_select_box.get())
        blur = self.get_textbox_value(self.smoothing_select_box.get())
        erode = self.get_textbox_value(self.outline_select_box.get())
        dither = self.dithering_bool.get()
        saturation = int(self.saturation_select_box.get())
        contrast = int(self.contrast_select_box.get())

        self.main.cv_image = convert(self.main.image_path, 
                                k=k, 
                                scale=scale, 
                                blur=blur, 
                                erode=erode, 
                                dither=dither, 
                                saturation=saturation, 
                                contrast=contrast)
        self.main.display.cv_to_pygame(self.main.cv_image)

    def transform_img_custom(self):
        k = self.value_entry_valid(int(self.color_num_entry.get()), 2, 128)
        saturation = self.value_entry_valid(int(self.saturation_entry.get()), -255, 255)
        contrast = self.value_entry_valid(int(self.contrast_entry.get()), -255, 255)
        # correct entry value
        self.color_num_entry.delete(0, "end")
        self.saturation_entry.delete(0, "end")
        self.contrast_entry.delete(0, "end")
        self.color_num_entry.insert(0, str(k))
        self.saturation_entry.insert(0, str(saturation))
        self.contrast_entry.insert(0, str(contrast))

        scale = int(self.pixel_size_select_box.get())
        blur = self.get_textbox_value(self.smoothing_select_box.get())
        erode = self.get_textbox_value(self.outline_select_box.get())
        dither = self.dithering_bool.get()

        self.main.cv_image = convert(self.main.image_path, 
                                k=k, 
                                scale=scale, 
                                blur=blur, 
                                erode=erode, 
                                dither=dither, 
                                saturation=saturation, 
                                contrast=contrast)
        self.main.display.cv_to_pygame(self.main.cv_image)

    def sign_entry_valid(self, sign):
        if sign == '':
            return 1
        elif sign[0] == '+':
            return 1
        elif sign[0] == '-':
            return -1

    def value_entry_valid(self, value, min_num=0, max_num=255):
        if value:
            value = max(value, min_num)
            value = min(value, max_num)
            return value
        else:
            if min_num > 0:
                return min_num
            else:
                return 0

    def get_textbox_value(self, text):
        if text == 'None':
            return 0
        elif text == 'Less':
            return 1
        elif text == 'Great':
            return 2

    def save_img(self):
        save_cv_img(self.main.cv_image, './', self.main.load_file_name.get() + '_pixel')

class Gui_helper_simple_page(Gui_helper_page_module):
    def __init__(self, master):
        Gui_helper_page_module.__init__(self, master)
        self.mode = 'Simple簡化'

        self.now_file_name = Label(self,textvariable=self.main.load_file_name)
        self.now_file_name.grid(column=0, row=0, sticky=N+W)

        self.import_img_btn = Button(self, text='import img導入圖片', command=self.import_img)
        self.import_img_btn.grid(column=4, row=0, sticky=E+N)

        # color num
        self.color_num_name = Label(self,text='Color nums色數')
        self.color_num_name.grid(column=0, row=1, sticky=N+W)
        self.color_num_select_box = Combobox(self, width=5)
        self.color_num_select_box.grid(column=0, row=2, sticky=N+W)
        self.color_num_select_box['values'] = ['2', '4', '8', '16','32','64', '128']
        self.color_num_select_box.current(0)
        # pixel size
        self.pixel_size_name = Label(self,text='Pixel size像素尺寸')
        self.pixel_size_name.grid(column=4, row=1, sticky=N+E)
        self.pixel_size_select_box = Combobox(self, width=5)
        self.pixel_size_select_box.grid(column=4, row=2, sticky=N+E)
        self.pixel_size_select_box['values'] = ['1', '2', '3', '4']
        self.pixel_size_select_box.current(0)
        # smoothing
        self.smoothing_name = Label(self,text='Smoothing光滑')
        self.smoothing_name.grid(column=0, row=3, sticky=N+W)
        self.smoothing_select_box = Combobox(self, width=5)
        self.smoothing_select_box.grid(column=0, row=4, sticky=N+W)
        self.smoothing_select_box['values'] = ['None', 'Less', 'Great']
        self.smoothing_select_box.current(0)
        # outlines
        self.outline_name = Label(self,text='Outline輪廓')
        self.outline_name.grid(column=4, row=3, sticky=N+E)
        self.outline_select_box = Combobox(self, width=5)
        self.outline_select_box.grid(column=4, row=4, sticky=N+E)
        self.outline_select_box['values'] = ['None', 'Less', 'Great']
        self.outline_select_box.current(0)
        # saturation
        self.saturation_name = Label(self,text='Saturation飽和')
        self.saturation_name.grid(column=0, row=5, sticky=N+W)
        self.saturation_select_box = Combobox(self, width=5)
        self.saturation_select_box.grid(column=0, row=6, sticky=N+W)
        self.saturation_select_box['values'] = ['-200', '-150', '-100', '-50', '0', '50', '100', '150', '200']
        self.saturation_select_box.current(len(self.saturation_select_box['values'])//2)
        # contrast
        self.contrast_name = Label(self,text='Contrast對比')
        self.contrast_name.grid(column=4, row=5, sticky=N+E)
        self.contrast_select_box = Combobox(self, width=5)
        self.contrast_select_box.grid(column=4, row=6, sticky=N+E)
        self.contrast_select_box['values'] = ['-200', '-150', '-100', '-50', '0', '50', '100', '150', '200']
        self.contrast_select_box.current(len(self.contrast_select_box['values'])//2)

        # dithering
        self.dithering_bool = BooleanVar()
        self.dithering_check = Checkbutton(self, text='Dithering顆粒抖動', variable=self.dithering_bool)
        self.dithering_check.grid(column=0, row=7, sticky=N+W)
        
        # transform button
        self.transform_img_btn = Button(self, text='transform變換', command=self.transform_img)
        self.transform_img_btn.grid(column=0, row=8, sticky=W+N)
        # save_img button
        self.save_img_btn = Button(self, text='save保存', command=self.save_img)
        self.save_img_btn.grid(column=0, row=9, sticky=W+N)
        
        # cutom mode
        self.custom_mode_button = Button(self, text='Custom mode自定義', command=self.custom_mode_switch)
        self.custom_mode_button.grid(column=0, row=10, sticky=N+W)

class Gui_helper_custom_page(Gui_helper_page_module):
    def __init__(self, master):
        Gui_helper_page_module.__init__(self, master)
        self.mode = 'Custom自定義'
        self.only_digit = self.main.only_digit_vcmd

        self.now_file_name = Label(self,textvariable=self.main.load_file_name)
        self.now_file_name.grid(column=0, row=0, sticky=N+W)

        self.import_img_btn = Button(self, text='import img導入圖片', command=self.import_img)
        self.import_img_btn.grid(column=4, row=0, sticky=E+N)

        # color num
        self.color_num_name = Label(self,text='Color nums色數')
        self.color_num_name.grid(column=0, row=1, sticky=N+W)
        self.color_num_entry = Entry(self, width=5, validate='key', validatecommand=self.only_digit)
        self.color_num_entry.grid(column=0, row=2, sticky=N+W)
        self.color_num_entry.insert(0, '2')
        # pixel size
        self.pixel_size_name = Label(self,text='Pixel size像素尺寸')
        self.pixel_size_name.grid(column=4, row=1, sticky=N+E)
        self.pixel_size_select_box = Combobox(self, width=5)
        self.pixel_size_select_box.grid(column=4, row=2, sticky=N+E)
        self.pixel_size_select_box['values'] = ['1', '2', '3', '4']
        self.pixel_size_select_box.current(0)
        # smoothing
        self.smoothing_name = Label(self,text='Smoothing光滑')
        self.smoothing_name.grid(column=0, row=3, sticky=N+W)
        self.smoothing_select_box = Combobox(self, width=5)
        self.smoothing_select_box.grid(column=0, row=4, sticky=N+W)
        self.smoothing_select_box['values'] = ['None', 'Less', 'Great']
        self.smoothing_select_box.current(0)
        # outlines
        self.outline_name = Label(self,text='Outline輪廓')
        self.outline_name.grid(column=4, row=3, sticky=N+E)
        self.outline_select_box = Combobox(self, width=5)
        self.outline_select_box.grid(column=4, row=4, sticky=N+E)
        self.outline_select_box['values'] = ['None', 'Less', 'Great']
        self.outline_select_box.current(0)
        # saturation
        self.saturation_name = Label(self,text='Saturation飽和')
        self.saturation_name.grid(column=0, row=5, sticky=N+W)
        self.saturation_entry = Entry(self, width=5, validate='key', validatecommand=self.only_digit)
        self.saturation_entry.grid(column=0, row=6, sticky=N+W)
        self.saturation_entry.insert(0, '0')
        # contrast
        self.contrast_name = Label(self,text='Contrast對比')
        self.contrast_name.grid(column=4, row=5, sticky=N+E)
        self.contrast_entry = Entry(self, width=5, validate='key', validatecommand=self.only_digit)
        self.contrast_entry.grid(column=4, row=6, sticky=N+E)
        self.contrast_entry.insert(0, '0')

        # dithering
        self.dithering_bool = BooleanVar()
        self.dithering_check = Checkbutton(self, text='Dithering顆粒抖動', variable=self.dithering_bool)
        self.dithering_check.grid(column=0, row=7, sticky=N+W)
        
        # transform button
        self.transform_img_btn = Button(self, text='transform變換', command=self.transform_img_custom)
        self.transform_img_btn.grid(column=0, row=8, sticky=W+N)
        # save_img button
        self.save_img_btn = Button(self, text='save保存', command=self.save_img)
        self.save_img_btn.grid(column=0, row=9, sticky=W+N)
        
        # simple mode
        self.simple_mode_button = Button(self, text='Simple mode簡化模式', command=self.simple_mode_switch)
        self.simple_mode_button.grid(column=0, row=10, sticky=N+W)