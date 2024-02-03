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
        """
        Создание уровня
        :return: игрок, монстры, х, у
        """
        new_player, x, y = None, None, None
        # Расстановка клеток и игрока
        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                Tile('empty', x, y)
                if self.level[y][x] == '#':  # Стенка
                    Wall(x, y)
                elif self.level[y][x] == '!':  # Пол-ошибка
                    Error(x, y)
                elif self.level[y][x] == '^':  # Финиш
                    Finish(x, y)
                elif self.level[y][x] == '@':  # Игрок
                    new_player = Player(x * tile_width, y * tile_height, self.size)
                    self.level[y][x] = '.'

        # Создание монстров
        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                if self.level[y][x] == 'W':  # Медленный баг
                    self.monsters.append(WarningEntity(x * tile_width, y * tile_height, new_player))
                    self.level[y][x] = '.'
                elif self.level[y][x] == 'E':  # Быстрый баг
                    self.monsters.append(ErrorEntity(x * tile_width, y * tile_height, new_player))
                    self.level[y][x] = '.'
                elif self.level[y][x] == 'D':  # Движущийся вниз
                    self.monsters.append(MovingEntity(x * tile_width, y * tile_height,
                                                      (x * tile_width, (y + 2) * tile_height)))
                    self.level[y][x] = '.'
                elif self.level[y][x] == 'U':  # Движущийся вверх
                    self.monsters.append(MovingEntity(x * tile_width, y * tile_height,
                                                      (x * tile_width, (y - 2) * tile_height)))
                    self.level[y][x] = '.'
                elif self.level[y][x] == 'R':  # Движущийся вправо
                    self.monsters.append(MovingEntity(x * tile_width, y * tile_height,
                                                      ((x + 2) * tile_width, y * tile_height)))
                    self.level[y][x] = '.'
                elif self.level[y][x] == 'L':  # Движущийся влево
                    self.monsters.append(MovingEntity(x * tile_width, y * tile_height,
                                                      ((x - 2) * tile_width, y * tile_height)))
                    self.level[y][x] = '.'
        # возвращение игрока, монстров
        return new_player, self.monsters, x, y


