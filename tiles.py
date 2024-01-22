#  Всё что относится к клеткам в игре находится тут
import pygame
from our_tools import load_image

tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('floor.png')
}

tile_width = tile_height = 64

tiles_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
