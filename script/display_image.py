import pygame
import cv2
import sys
import re
from settings import resource_path, sample_image_path

class Display_image:
    def __init__(self, width=500, height=500):
        pygame.init()
        self.display_screen_resize(width, height)
        pygame.display.set_caption("Display Screen")
        pygame.display.set_icon(pygame.image.load(resource_path("assets\icon\icon.png")))

        self.limit_size = [800, 600]
        self.or_image = pygame.image.load(resource_path(sample_image_path)).convert_alpha()
        self.image = pygame.image.load(resource_path(sample_image_path)).convert_alpha()
        self.new_x = 0
        self.new_y = 0
        self.scale_rate = 1
        self.scale_image()
        self.image_drag = False

    def image_load(self, image_path):
        image_path.replace("\\", "/")
        file_name = re.split("/", image_path)[-1]
        file_format = file_name.split('.')[-1]
        if not file_format in ['mp4', 'avi', 'flv']:
            self.or_image = pygame.image.load(image_path)
            self.scale_image()

    def display_screen_resize(self, width=10, height=10, mode=0):
        if mode == 0:
            self.display_screen = pygame.display.set_mode((width, height))
        elif mode == 1:
            self.image_resize_limit()
            self.display_screen = pygame.display.set_mode(self.image.get_size())

    def image_resize_limit(self):
        self_image_size = self.image.get_size()
        x_rate = 1
        y_rate = 1
        new_rate = 1
        if self_image_size[0] > self.limit_size[0]:
            x_rate = self.limit_size[0] / self_image_size[0]
        if self_image_size[1] > self.limit_size[1]:
            y_rate = self.limit_size[1] / self_image_size[1]
        new_rate = min(x_rate, y_rate)
        self.or_scale_rate = new_rate
        self.image = pygame.transform.scale(self.or_image, (self_image_size[0]*new_rate, self_image_size[1]*new_rate))
        self.scale_image()

    def cv_to_pygame(self, cv_img):
        frame = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        frame = cv2.transpose(frame)
        frame = pygame.surfarray.make_surface(frame)
        self.or_image = frame
        self.scale_image()

    def display_update(self):
        self.display_screen.fill('black')
        if self.display_screen.get_size() != self.image.get_size():
            self.display_screen_resize(mode=1)
        self.display_screen.blit(self.scaled_image, self.scaled_image_rect)
        pygame.display.update()

    def scale_image(self):
        image_size = self.image.get_size()
        self.scaled_image = pygame.transform.scale(self.or_image, (image_size[0]*self.scale_rate, image_size[1]*self.scale_rate))
        self.scaled_image_rect = self.scaled_image.get_rect(topleft = (self.new_x, self.new_y))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.scaled_image_rect.collidepoint(event.pos):
                            self.image_drag = True
                    elif event.button == 2:
                        self.new_x = 0
                        self.new_y = 0
                        self.scale_rate = 1
                        self.scale_image()
                    elif event.button == 4:
                        self.scale_rate += 0.1
                        self.scale_image()
                    elif event.button == 5:
                        self.scale_rate -= 0.1
                        if self.scale_rate < 0:
                            self.scale_rate = 0
                        self.scale_image()
                    # 1 - left click
                    # 2 - middle click
                    # 3 - right click
                    # 4 - scroll up
                    # 5 - scroll down
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.image_drag = False
                if event.type == pygame.MOUSEMOTION:
                    if self.image_drag:
                        self.scaled_image_rect.move_ip(event.rel)
                        self.new_x = self.scaled_image_rect[0]
                        self.new_y = self.scaled_image_rect[1]
            self.display_update()

    def quit(self):
        pygame.quit()
        sys.exit()