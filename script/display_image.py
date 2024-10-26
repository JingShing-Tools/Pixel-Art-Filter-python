import pygame
import cv2
import sys
import re
from settings import resource_path, sample_image_path

class Display_image:
    def __init__(self, width=500, height=500):
        pygame.init()
        self.new_x, self.new_y = 0, 0
        self.scale_rate = 1
        self.image_drag = False
        self.display_screen_resize(width, height)
        pygame.display.set_caption("Display Screen")
        pygame.display.set_icon(pygame.image.load(resource_path("assets/icon/icon.png")))

        self.limit_size = [800, 600]
        self.image_path = resource_path(sample_image_path)
        self.load_initial_image()

    def load_initial_image(self):
        self.or_image = pygame.image.load(self.image_path).convert_alpha()
        self.image = self.or_image.copy()
        self.scale_image()

    def image_load(self, image_path):
        image_path = image_path.replace("\\", "/")
        if not image_path.split('.')[-1] in ['mp4', 'avi', 'flv']:
            self.or_image = pygame.image.load(image_path).convert_alpha()
            self.scale_image()

    def display_screen_resize(self, width=10, height=10, mode=0):
        if mode == 0:
            self.display_screen = pygame.display.set_mode((width, height))
        elif mode == 1:
            self.image_resize_limit()
            self.display_screen = pygame.display.set_mode(self.image.get_size())

    def image_resize_limit(self):
        img_size = self.image.get_size()
        x_rate = self.limit_size[0] / img_size[0] if img_size[0] > self.limit_size[0] else 1
        y_rate = self.limit_size[1] / img_size[1] if img_size[1] > self.limit_size[1] else 1
        self.scale_rate = min(x_rate, y_rate)
        self.image = pygame.transform.scale(self.or_image, (int(img_size[0] * self.scale_rate), int(img_size[1] * self.scale_rate)))
        self.scale_image()

    def cv_to_pygame(self, cv_img):
        rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        self.or_image = pygame.surfarray.make_surface(rgb_img.swapaxes(0, 1))
        self.scale_image()

    def display_update(self):
        self.display_screen.fill('black')
        self.display_screen.blit(self.scaled_image, self.scaled_image_rect)
        pygame.display.update()

    def scale_image(self):
        img_size = self.image.get_size()
        self.scaled_image = pygame.transform.scale(self.or_image, (int(img_size[0] * self.scale_rate), int(img_size[1] * self.scale_rate)))
        self.scaled_image_rect = self.scaled_image.get_rect(topleft=(self.new_x, self.new_y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.scaled_image_rect.collidepoint(event.pos):
                    self.image_drag = True
                elif event.button == 2:
                    self.reset_image()
                elif event.button == 4:
                    self.scale_rate += 0.1
                    self.scale_image()
                elif event.button == 5:
                    self.scale_rate = max(0.1, self.scale_rate - 0.1)
                    self.scale_image()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.image_drag = False
            elif event.type == pygame.MOUSEMOTION and self.image_drag:
                self.scaled_image_rect.move_ip(event.rel)
                self.new_x, self.new_y = self.scaled_image_rect.topleft

    def reset_image(self):
        self.new_x, self.new_y, self.scale_rate = 0, 0, 1
        self.scale_image()

    def run(self):
        while True:
            self.handle_events()
            self.display_update()

    def quit(self):
        pygame.quit()
        sys.exit()
