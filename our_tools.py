import os
import pygame

all_sprites = pygame.sprite.Group()  # специально группа тут, чтобы не было цикличного импортирования
pygame.init()
pygame.display.set_mode((600, 400))


def load_image(name, color_key=None):
    """
    Функция для загрузки картинок
    :param name: название файла без "data"
    :param color_key: Игнорирование цвета
    :return: возвращает картинку
    """
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


def collision_test(obj, tiles, mask=False):
    """
    Функция для откработки коллизии
    :param obj: кто касается
    :param tiles: кого должны коснуться
    :param mask: использовать режим маски? Нужен для более крутого колайда, но нельзя использовать на стенках
    :return: кого коснулись
    """
    hit_list = []
    if mask:
        for tile in tiles:
            if pygame.sprite.collide_mask(obj, tile):
                hit_list.append(tile)
        return hit_list
    else:
        for tile in tiles:
            rect = obj.rect
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list
