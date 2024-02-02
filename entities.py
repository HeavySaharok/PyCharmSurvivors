#  Классы различных сущностей находятся тут
import pygame
from our_tools import all_sprites, collision_test, load_image
from tiles import obstacle_group, finish_group, error_group

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
    def __init__(self, x, y, point_b: (int, int)):
        super().__init__(load_image('moving_error.png'), 1, 1, x, y)
        error_group.add(self)
        point_a = (x, y)
        self.x0, self.x1 = point_a[0], point_b[0]
        self.y0, self.y1 = point_a[1], point_b[1]
        self.spd = 1
        self.hitbox = (self.rect.x, self.rect.y, 32, 32)
        self.dir_x = True
        self.dir_y = True

    def move(self):
        x = self.rect.x
        y = self.rect.y
        if self.y0 - self.y1:
            if self.dir_y:
                if y == self.y1:
                    self.dir_y = False
                self.rect.y += self.spd
            else:
                if y == self.y0:
                    self.dir_y = True
                self.rect.y -= self.spd

        if self.x0 - self.x1:
            if self.dir_x:
                if x == self.x1:
                    self.dir_x = False
                self.rect.x += self.spd
            else:
                if x == self.x0:
                    self.dir_x = True
                self.rect.x -= self.spd