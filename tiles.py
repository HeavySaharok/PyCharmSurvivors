#  Всё что относится к клеткам в игре находится тут
import pygame
from our_tools import load_image, all_sprites

tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('floor.png'),
    'finish': load_image('finish.png'),
    'error': load_image('error_floor.png')
}

tile_width = tile_height = 64
tiles_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
finish_group = pygame.sprite.Group()
error_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, *arg):
        super().__init__(tiles_group, all_sprites, *arg)
        self.image = tile_images[tile_type]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall(Tile):
    def __init__(self, pos_x, pos_y):
        super().__init__('wall', pos_x, pos_y, obstacle_group)


class Finish(Tile):
    def __init__(self, pos_x, pos_y):
        super().__init__('finish', pos_x, pos_y, finish_group)


class Error(Tile):
    def __init__(self, pos_x, pos_y):
        super().__init__('error', pos_x, pos_y, error_group)
