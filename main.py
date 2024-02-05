import pygame.time
import sqlite3
import os
import sys
import pygame


class Levels:
    # создание кнопок
    def __init__(self, width, height, username):
        self.height = height
        self.width = width
        self.username = username
        # значения по умолчанию
        self.left = 55
        self.top = 300
        self.cell_size = 85
        self.rects = []

    def render(self, scr):
        c = 0
        for y in range(1, self.width + 1):
            for x in range(self.height):
                c += 1
                font = pygame.font.Font(None, 40)
                scr.blit(font.render(str(c) + '.lvl', True, pygame.Color(123, 104, 238)),
                         (x * self.cell_size * 1.45 + 68,
                          (y - 1) * self.cell_size + self.top + 45, self.cell_size, self.cell_size))
                rect = pygame.draw.rect(scr, pygame.Color(0, 255, 0), (
                    x * self.cell_size * 1.45 + 50, (y - 1) * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 3)
                if len(self.rects) < self.width * self.height:
                    self.rects.append([rect.topleft, rect.topright, rect.bottomleft])

    def get_cell(self, mouse_pos):
        num_lvl = 0
        for i in range(len(self.rects)):
            if (self.rects[i][0][0] <= mouse_pos[0] <= self.rects[i][1][0]) and (
                    self.rects[i][0][1] <= mouse_pos[1] <= self.rects[i][2][1]):
                num_lvl = i + 1

        return num_lvl

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            return cell - 1, self.username


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(lvl, username):
    """
    Вызвать из начала игры один раз:
    :return: username
    """
    screen.fill(pygame.Color('white'))
    intro_text = ["", "",
                  "Введите Ваше имя:", "",
                  "ПРАВИЛА: избегай багов и выберись живым",
                  f"ВЫБЕРИТЕ УРОВЕНЬ: до {lvl}"]
    fon = pygame.image.load('data/logo-2.png')
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 36)
    text_coord = 60
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 80
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    base_font = pygame.font.Font(None, 32)
    user_text = username

    input_rect = pygame.Rect(80, 170, 140, 32)
    color_active = pygame.Color("#3CB371")

    color_passive = pygame.Color("#006400")
    active = False

    levels = Levels(lvl // 3, lvl // (lvl // 3), username)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = levels.get_click(event.pos)
                if click is None:
                    pass
                else:
                    pygame.quit()
                    return click

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
                levels.username = user_text

        if active:
            color = color_active
        else:
            color = color_passive

        pygame.draw.rect(screen, color, input_rect)
        text_surface = base_font.render(user_text, True, "black")

        # рендеринг согласно вводу мени пользователя
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = max(100, text_surface.get_width() + 10)

        levels.render(screen)
        pygame.display.flip()


ll = 15
WIDTH, HEIGHT = size = 640, 900
pygame.init()
FPS = 50
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode(size)
pygame.display.set_caption('PyCharm Survivors')


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


def result_screen(player_name: str):
    """
    Вызываем экран результатов
    :param player_name: имя текущего игрока
    :return:
    """
    pygame.init()
    unique = -2
    size = 630, 360
    screen = pygame.display.set_mode(size)
    fon = load_image('result_screen.png')
    screen.fill('Black')
    screen.blit(fon, (0, 0))
    pygame.display.set_caption('Results')
    players = Database('players.sqlite')
    result_text = [('#   ', 'Имя         ', 'Счёт')]
    lis = sorted(players.get_val('scores', '*', '')[:10], key=lambda x: x[2], reverse=True)
    for i in range(len(lis)):
        _, name, score = lis[i]
        if name == player_name:
            unique = i
        if len(name) > 10:
            name = name[:7] + '...'
        result_text.append((str(i + 1), name, str(score)))

    font = pygame.font.Font(None, 30)
    text_coord = 27
    for i in range(len(result_text)):
        place, name, score = result_text[i]
        if i - 1 == unique:
            p_rendered = font.render(place, 1, pygame.Color('Red'))
            n_rendered = font.render(name, 1, pygame.Color('Red'))
            s_rendered = font.render(score, 1, pygame.Color('Red'))
        else:
            p_rendered = font.render(place, 1, pygame.Color('White'))
            n_rendered = font.render(name, 1, pygame.Color('White'))
            s_rendered = font.render(score, 1, pygame.Color('White'))

        p_rect, n_rect, s_rect = p_rendered.get_rect(), n_rendered.get_rect(), s_rendered.get_rect()
        text_coord += 10
        p_rect.top, n_rect.top, s_rect.top = [text_coord] * 3
        p_rect.x, n_rect.x, s_rect.x = 10, 33, 133
        text_coord += p_rect.height
        screen.blit(p_rendered, p_rect)
        screen.blit(n_rendered, n_rect)
        screen.blit(s_rendered, s_rect)
    pygame.draw.line(screen, 'White', (0, 30), (0, 360), 3)
    pygame.draw.line(screen, 'White', (30, 30), (30, 360), 3)
    pygame.draw.line(screen, 'White', (130, 30), (130, 360), 3)
    pygame.draw.line(screen, 'White', (230, 30), (230, 360), 3)
    if unique != -2:
        congrats = f'Вы заняли {unique + 1} место!!!'
    else:
        congrats = 'Вы не попали в топ 10!'
    cong_ot = font.render(congrats, 1, pygame.Color('Red'))
    cong_rec = cong_ot.get_rect()
    cong_rec.y = 5
    cong_rec.x = (230 - cong_rec.width) // 2
    screen.blit(cong_ot, cong_rec)
    for j in range(12):
        pygame.draw.line(screen, 'White', (0, 30 * j + 30), (230, 30 * j + 30), 3)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()


def level_cleared(score: int):
    """
    Выводит поздравление с прохождением уровня и показывает кол-во очков.
    :param score: Кол-во очков ирока
    :return:
    """
    pygame.init()
    respar = 128
    size = w, h = 800, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Congrats!')
    end_text = ['Уровень пройден! Нажмите ПРОБЕЛ что бы перейти на следующий,',
                'или ESC если вы хотите закончить игру.']
    winner = pygame.transform.scale(load_image('winner.png'), (respar, respar))

    # картинка пока временная, надо нарисовать победную позу.

    screen.blit(winner, ((w - respar) // 2, 250))
    font = pygame.font.SysFont('Georgia', 23)
    y = 420
    for line in end_text:
        string_rendered = font.render(line, 1, pygame.Color(243, 255, 29))
        intro_rect = string_rendered.get_rect()
        y += 20
        intro_rect.top = y
        intro_rect.x = (w - intro_rect.width) // 2
        screen.blit(string_rendered, intro_rect)
    font = pygame.font.SysFont('Georgia', 50)
    string_rendered = font.render('Ваш результат: ' + str(score), 1, pygame.Color(243, 255, 29))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 100
    intro_rect.x = (w - intro_rect.width) // 2
    screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.quit()
                    return 1
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return 0
        pygame.display.flip()


def game_over():
    """
    Экран проигрыша.
    :return:
    """
    pygame.init()
    # Параметр нового размера картинки
    respar = 96
    size = w, h = 800, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Game over')
    res_text = ['Вы проиграли. Нажмите ПРОБЕЛ что бы начать уровень заново', 'или ESC если вы хотите закончить игру.']
    fon = pygame.transform.scale(load_image('gmov.png'), (w, h))
    screen.blit(fon, (0, -80))
    looser = pygame.transform.scale(load_image('Ninja.png').subsurface(pygame.Rect((0, 6 * 16), (16, 16))),
                                    (respar, respar))
    screen.blit(looser, ((w - respar) // 2, 340))
    font = pygame.font.SysFont('Georgia', 23)
    y = 420
    for line in res_text:
        string_rendered = font.render(line, 1, pygame.Color(243, 255, 29))
        intro_rect = string_rendered.get_rect()
        y += 20
        intro_rect.top = y
        intro_rect.x = (w - intro_rect.width) // 2
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.quit()
                    return 1
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return 0
        pygame.display.flip()


if __name__ == '__main__':
    result_screen('123')

all_sprites = pygame.sprite.Group()  # специально группа тут, чтобы не было цикличного импортирования
pygame.init()
pygame.display.set_mode((600, 400))


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


pygame.init()

entity_group = pygame.sprite.Group()


class Entity(pygame.sprite.Sprite):
    """Родовой класс всех созданий наших, тут множество переменных, анимация и наследование от спрайта
    А ещё оно само вырезает спрайты из спрайт-листа"""
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites, entity_group)
        self.times = 0
        self.spd = 2
        self.frames = []
        self.dir = 1
        self.ud = 0
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.mask = pygame.mask.from_surface(self.image)

    def cut_sheet(self, sheet, columns, rows):
        """
        Резка спрайтов
        :param sheet:
        :param columns:
        :param rows:
        :return:
        """
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.h * i, self.rect.w * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        if self.times % 6 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.times = 0
        self.times += 1


class Player(Entity):
    """
    Игрок, мы можем им управлять!
    (НЕ рекомендую делать больше одного игрока)
    """
    def __init__(self, x, y, map_size):
        super().__init__(load_image("ninja_walking_small.png"), 4, 4, x, y)
        self.map_size = map_size
        self.spd = 4
        self.standing = 0
        self.collis = 0

    def move(self, keys):
        """
        Передвежение игрока
        :param keys:
        :return:
        """
        self.standing = 0
        for key in keys:
            # Настройка кнопок
            if key == pygame.K_UP and self.rect.top >= 0:
                if self.dir != 1:
                    self.dir = 1
                self.rect.y -= self.spd

            elif key == pygame.K_DOWN and self.rect.bottom <= self.map_size[1]:
                if self.dir != 0:
                    self.dir = 0
                self.rect.y += self.spd

            elif key == pygame.K_RIGHT and self.rect.right <= self.map_size[0]:
                if self.dir != 3:
                    self.dir = 3
                self.rect.x += self.spd

            elif key == pygame.K_LEFT and self.rect.left >= 0:
                if self.dir != 2:
                    self.dir = 2
                self.rect.x -= self.spd

            # Проверка на столкновение
            if hits := collision_test(self, obstacle_group):  # Если есть столкновения, запись в переменную hits
                for elem in hits:
                    if key == pygame.K_UP:
                        self.rect.top = elem.rect.bottom
                    if key == pygame.K_DOWN:
                        self.rect.bottom = elem.rect.top
                    if key == pygame.K_LEFT:
                        self.rect.left = elem.rect.right
                    if key == pygame.K_RIGHT:
                        self.rect.right = elem.rect.left

            if collision_test(self, finish_group):
                self.collis = 2
                pygame.quit()
            elif collision_test(self, error_group, mask=True):
                self.collis = 1
                pygame.quit()
            else:
                self.collis = 0

    def update(self):
        if self.standing:
            self.cur_frame = 0
            self.image = self.frames[self.dir]
        elif self.times % 4 == 0:
            self.cur_frame = (self.cur_frame + 1) % 4
            self.image = self.frames[self.dir + self.cur_frame * 4]
            self.times = 0
        self.times += 1
        return self.collis


class WarningEntity(Entity):
    """Наш враг, суть которого в том что он всегда знает где мы и медленно следует за нами... очень медленно."""
    def __init__(self, x, y, victim):
        super().__init__(load_image('warning.png'), 4, 5, x, y)
        error_group.add(self)
        self.victim = victim
        self.spd = 1

    def move(self):
        x, y = self.victim.rect.center  # узнаём координаты жертвы
        dir_x = x - self.rect.center[0]
        dir_y = y - self.rect.center[1]
        # делим число на его модуль, чтобы узнать направление и умножаем на скорость
        if dir_x:
            self.rect.x += dir_x // abs(dir_x) * self.spd
        if dir_y:
            self.rect.y += dir_y // abs(dir_y) * self.spd


class ErrorEntity(Entity):
    """Наш враг, суть которого в том что он всегда знает где мы и очень быстро летит за нами... но из-за такой скорости
    он очень неуклюжий"""
    def __init__(self, x, y, victim, speed_limit=30, speed_control=3):
        super().__init__(load_image('error.png'), 11, 1, x, y)
        error_group.add(self)
        self.victim = victim
        self.spd_y = 0
        self.spd_x = 0
        self.acc = 1
        self.spd_lim = speed_limit
        self.spd_cont = speed_control
        self.hitbox = (self.rect.x, self.rect.y, 32, 32)

    def move(self):
        x, y = self.victim.rect.center  # узнаём координаты жертвы
        dir_x = x - self.rect.center[0]
        dir_y = y - self.rect.center[1]
        self.hitbox = (self.rect.x, self.rect.y, 32, 32)
        # делим число на его модуль, чтобы узнать направление и умножаем на скорость
        if dir_x:
            self.spd_x += dir_x // abs(dir_x) * self.acc
        if dir_y:
            self.spd_y += dir_y // abs(dir_y) * self.acc
        if self.spd_x > self.spd_lim:
            self.spd_x = self.spd_lim
        if self.spd_y > self.spd_lim:
            self.spd_y = self.spd_lim

        self.rect.x += self.spd_x // self.spd_cont
        self.rect.y += self.spd_y // self.spd_cont


class MovingEntity(Entity):
    """Этот враг не обладает интелектом, он просто сделуеть из точки A в точку Б"""
    def __init__(self, x, y, point_b: (int, int), spd=1):
        super().__init__(load_image('moving_error.png'), 1, 1, x, y)
        error_group.add(self)
        point_a = (x, y)
        self.x0, self.x1 = (point_a[0], point_b[0]) if point_a[0] < point_b[0] else (point_b[0], point_a[0])
        self.y0, self.y1 = (point_a[1], point_b[1]) if point_a[1] > point_b[1] else (point_b[1], point_a[1])
        self.spd = spd
        self.hitbox = (self.rect.x, self.rect.y, 32, 32)
        self.dir_x = False
        self.dir_y = False

    def move(self):
        x = self.rect.x
        y = self.rect.y
        if self.y0 - self.y1:
            if self.dir_y:
                if y >= self.y0:
                    self.dir_y = False
                self.rect.y += self.spd
            else:
                if y <= self.y1:
                    self.dir_y = True
                self.rect.y -= self.spd

        if self.x0 - self.x1:
            if self.dir_x:
                if x >= self.x1:
                    self.dir_x = False
                self.rect.x += self.spd
            else:
                if x <= self.x0:
                    self.dir_x = True
                self.rect.x -= self.spd


class Database:
    def __init__(self, db_name: str, path=''):
        """
        Забираем базу из указанного места, если она лежит в корневой папке, то нужно лишь её название.
        """
        self.name = path + db_name
        self.db = sqlite3.connect(self.name)
        self.cur = self.db.cursor()

    def insert(self, tab_name: str, fields: tuple, values: tuple):
        """
         Функция, что бы добавить новый объект в базу.
        :param tab_name: Название таблицы
        :param fields: названия полей, в которые вставляем значения
        :param values: сами значения
        """

        self.cur.execute(f'INSERT INTO {tab_name}{fields} VALUES{values}')

    def new_table(self, tab_name: str, *keys: str):
        """
        Функция по созданию новой таблицы в базе. На вход подаётся её название, ключи в формате '(ключ + свойства)'
        Например мы хотим добавить таблицу с игроками. Тогда мы пишем так:
        new_table('players', 'id INTEGER PRIMARY KEY', 'name TEXT NOT NULL')
        :param tab_name: название таблицы
        :param keys: названия колонок
        """
        vals = ', '.join(keys)
        self.cur.execute(f'CREATE TABLE IF NOT EXISTS {tab_name} ({vals})')

    def get_val(self, tab_name: str, column: str, condition=''):
        """
        Получаем значения из таблицы по заданным условиям. Сомневаюсь, что будем ей пользоваться т.к. условия, как
        правило, слишком сложные, что бы запихнуть их в 1 строку.
        :param tab_name: Название таблицы
        :param column: Колонка с забираемым значением
        :param condition: Условие, при котором забираем значение
        :return: Кортеж с данными(вроде как)
        """
        if not condition:
            return self.cur.execute(f'SELECT {column} from {tab_name}').fetchall()
        else:
            return self.cur.execute(f'SELECT {column} from {tab_name}'
                                    f' WHERE {condition}').fetchone()

    def remove(self, tab_name: str, condition: str):
        """
        Удаляем поле таблицы, удовлетворяющее требованиям. Оставьте condition пустым, если хотите очистить таблицу.
        :param tab_name: Название таблицы.
        :param condition: Условие, при котором убираем значение.
        :return: None
        """
        if condition:
            self.cur.execute(f'DELETE from {tab_name} WHERE {condition}')

    def update_score(self, tabname: str, name: str, score: int):
        """
        Обновляем очки в таблице.
        :param tabname: Название таблицы.
        :param name: Имя игрока для обновления
        :param score: Новый результат
        :return:
        """
        if name in list(map(lambda x: list(x)[0], self.get_val(tabname, 'name'))):
            if score > self.get_val(tabname, 'score', f'name = "{name}"')[0]:
                self.cur.execute(f'UPDATE {tabname}'
                                 f' SET score = {score}'
                                 f' WHERE name = "{name}"')
        else:
            self.insert(tabname, ('name', 'score'), (name, score))

    def close(self):
        self.db.commit()


FPS = 60


direct = []
running = True
# присваивание уровня и имени пользователя
lv_id, username = start_screen(3, '')
score = 0
bounty = 5000
levels = ['1.map', '2.map', '3.map']
lev_done = 0


def clear_level():
    """
    Функция, чтобы очищать группы спрайтов и т.п.
    :return:
    """
    obstacle_group.empty()
    all_sprites.empty()
    entity_group.empty()
    tiles_group.empty()
    error_group.empty()
    finish_group.empty()


# Карта
def show(level_name):
    global bounty
    bounty = 5000
    pygame.init()
    # музыка
    pygame.mixer.music.load('data/Cello.ogg')
    pygame.mixer.music.play(-1)
    level_map = [list(el) for el in load_level(level_name)]
    mape = Map(level_map)
    # экран
    sc = pygame.display.set_mode(mape.size)
    pygame.display.set_caption(level_name)
    return mape.generate_level() + (sc, pygame.time.Clock())


hero, monsters, level_x, level_y, screen, clock = show(levels[lv_id])
# основной цикл
while running:
    if lev_done:
        pygame.quit()
        a = level_cleared(score)
        lev_done = 0
        if not a:
            running = 0
    screen.fill(pygame.Color("black"))
    if direct:
        hero.move(direct)
    else:
        hero.standing = 1
    for monster in monsters:
        monster.move()
    all_sprites.update()
    if hero.collis == 1:
        clear_level()
        pygame.quit()
        direct = []
        score = 0
        a = game_over()
        if not a:
            break
        else:
            hero, monsters, level_x, level_y, screen, clock = show(levels[lv_id])
            direct = []
    elif hero.collis == 2:
        clear_level()
        pygame.quit()
        direct = []
        score += int(bounty)
        a = level_cleared(score)
        if not a:
            break
        else:
            lv_id += 1
            if lv_id == len(levels):
                break
            else:
                pygame.quit()
                hero, monsters, level_x, level_y, screen, clock = show(levels[lv_id])
    tiles_group.draw(screen)
    obstacle_group.draw(screen)
    entity_group.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            direct.append(event.key)
        if event.type == pygame.KEYUP and event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            direct.pop(direct.index(event.key))
    clock.tick(FPS)
    bounty -= 1
    pygame.display.flip()

# Вызов экрана конца игры. Теперь никнейм берётся из стартскрина, а очки в переменной score.
pygame.quit()
if username != '':
    players = Database('players.sqlite')
    players.update_score('scores', username, score)
    players.close()
    result_screen(username)
    pygame.quit()
