# Код карты
from tiles import *
from entities import *


def load_level(filename):
    """
    Функция загрузки уровня
    :param filename: название файла уровня
    :return: Матрица карты
    """
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Map:
    """
    Класс карты
    """
    def __init__(self, level_map):
        self.level = level_map
        self.size = (max(len(el) for el in level_map) * tile_width, len(level_map) * tile_height)
        self.monsters = []

    def generate_level(self):
        new_player, x, y = None, None, None
        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                Tile('empty', x, y)
                if self.level[y][x] == '#':
                    Wall(x, y)
                elif self.level[y][x] == '!':
                    Error(x, y)
                elif self.level[y][x] == '^':
                    Finish(x, y)
                elif self.level[y][x] == '@':
                    new_player = Player(load_image("ninja_walking.png"), 4, 4,
                                        x * tile_width, y * tile_height, self.size)
                    self.level[y][x] = '.'
        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                if self.level[y][x] == 'W':
                    self.monsters.append(WarningEntity(x * tile_width, y * tile_height, new_player))
                    self.level[y][x] = '.'
                elif self.level[y][x] == 'E':
                    self.monsters.append(ErrorEntity(x * tile_width, y * tile_height, new_player))
                    self.level[y][x] = '.'
        # вернем игрока, а также размер поля в клетках
        return new_player, self.monsters, x, y


