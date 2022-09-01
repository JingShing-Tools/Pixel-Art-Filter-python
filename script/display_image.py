import pygame
import cv2
import sys
from settings import resource_path

class Display_image:
    def __init__(self, width=500, height=500):
        pygame.init()
        self.display_screen_resize(width, height)
        pygame.display.set_caption("Display Screen")
        pygame.display.set_icon(pygame.image.load(resource_path("assets\icon\icon.png")))

        self.image = pygame.transform.scale(pygame.image.load(resource_path("assets\image\\0.png")).convert_alpha(), (width, height))

    def image_load(self, image_path):
        self.image = pygame.image.load(image_path)

    def display_screen_resize(self, width=10, height=10, mode=0):
        if mode == 0:
            self.display_screen = pygame.display.set_mode((width, height))
        elif mode == 1:
            self.display_screen = pygame.display.set_mode(self.image.get_size())


    def cv_to_pygame(self, cv_img):
        frame = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        frame = cv2.transpose(frame)
        frame = pygame.surfarray.make_surface(frame)
        self.image = frame

    def display_update(self):
        if self.display_screen.get_size() != self.image.get_size():
            self.display_screen_resize(mode=1)
        self.display_screen.blit(self.image, (0, 0))
        pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.display_update()