from numpy import random
import pygame
from Classes.constants import SCALE_FACTOR, WORLD_HEIGHT, WORLD_WIDTH


class Water:
    def __init__(self):
        rect = self.generate_water_rect()
        while self.rect_covers_start_pos(rect):
            rect = self.generate_water_rect()
        self.rect = rect

    def generate_water_rect(self):
        randomcenter_x = random.randint(0, WORLD_WIDTH)
        randomcenter_y = random.randint(0, WORLD_HEIGHT)
        random_size = random.randint(30, 100)
        return pygame.Rect(randomcenter_x, randomcenter_y, random_size, random_size)

    def rect_covers_start_pos(self, rect):
        if rect.midtop[1] < WORLD_HEIGHT / 2 and rect.midbottom[1] > WORLD_WIDTH / 2:
            return True
        else:
            return False