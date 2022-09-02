from pixel_converter import *
from gui_helper_new import *
from display_image import Display_image

if __name__ == '__main__':
    display = Display_image()
    from threading import Thread
    def gui_run():
        gui_help = Gui_helper_main(display)
        gui_help.run()
    thread1 = Thread(target=gui_run)
    thread1.setDaemon(True)
    thread1.start()
    display.run()