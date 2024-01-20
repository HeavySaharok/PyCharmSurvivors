# Код карты
from tiles import Tile, Player


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Map:
    def __init__(self, level_map):
        self.level = level_map

    def generate_level(self):
        new_player, x, y = None, None, None
        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                if self.level[y][x] == '#':
                    Tile('wall', x, y)
                elif self.level[y][x] == '@':
                    Tile('empty', x, y)
                    new_player = Player(x, y)
                    self.level[y][x] = '.'
        # вернем игрока, а также размер поля в клетках
        return new_player, x, y


