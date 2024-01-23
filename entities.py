#  Классы различных сущностей находятся тут
import pygame
from our_tools import all_sprites, collision_test, next_level
from tiles import obstacle_group, finish_group, error_group

pygame.init()

entity_group = pygame.sprite.Group()


class Entity(pygame.sprite.Sprite):

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

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * j, self.rect.h * i)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        if self.times % 6 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.times = 0
        self.times += 1


class Player(Entity):

    def __init__(self, sheet, columns, rows, x, y, map_size):
        super().__init__(sheet, columns, rows, x, y)
        self.map_size = map_size
        self.spd = 4
        self.standing = 0

    def move(self, keys):
        self.standing = 0
        for key in keys:

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

            if hits := collision_test(self.rect, obstacle_group):
                for elem in hits:
                    if key == pygame.K_UP:
                        self.rect.top = elem.rect.bottom
                    if key == pygame.K_DOWN:
                        self.rect.bottom = elem.rect.top
                    if key == pygame.K_LEFT:
                        self.rect.left = elem.rect.right
                    if key == pygame.K_RIGHT:
                        self.rect.right = elem.rect.left

            if collision_test(self.rect, finish_group):
                next_level('name')
                print('finish')

            if collision_test(self.rect, error_group):
                print('Умер')
                raise 'KEK'

    def update(self):
        if self.standing:
            self.cur_frame = 0
            self.image = self.frames[4 * self.dir + self.cur_frame]
        elif self.times % 4 == 0:
            self.cur_frame = (self.cur_frame + 1) % 4
            self.image = self.frames[4 * self.dir + self.cur_frame]
            self.times = 0
        self.times += 1
