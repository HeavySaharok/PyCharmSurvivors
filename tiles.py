#  Всё что относится к клеткам в игре находится тут
import pygame
from our_tools import load_image

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}

tile_width = tile_height = 50

tiles_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


player_image = load_image('mario.png')
player_group = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = pos_x, pos_y

    def move(self, x, y):
        self.pos = x, y
        self.rect.x = x * tile_width + 15
        self.rect.y = y * tile_height + 5
        print(self.pos)