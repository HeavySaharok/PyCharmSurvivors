import os
import pygame

all_sprites = pygame.sprite.Group()  # специально группа тут, чтобы не было цикличного импортирования
pygame.init()
pygame.display.set_mode((600, 400))


def load_image(name, color_key=None):

    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image
