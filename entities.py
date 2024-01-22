#  Классы различных сущностей находятся тут
import pygame

from our_tools import load_image
from tiles import tile_width, tile_height


class Entity:
    pass


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