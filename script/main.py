from pixel_converter import *
from gui_helper_new import *
from display_image import Display_image
from threading import Thread

def gui_run(display):
    gui_helper = Gui_helper_main(display)
    gui_helper.run()

if __name__ == '__main__':
    display = Display_image()
    thread1 = Thread(target=gui_run, args=(display,), daemon=True)
    thread1.start()
    display.run()
