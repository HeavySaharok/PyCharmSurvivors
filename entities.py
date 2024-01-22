#  Классы различных сущностей находятся тут
import pygame
from our_tools import all_sprites


pygame.init()


class Entity:
    pass


class AnimatedSprite(pygame.sprite.Sprite):

    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.times = 0
        self.spd = 2
        self.frames = []
        self.lr = 1
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        if self.times % 6 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.times = 0
        self.times += 1

    def move(self, keys):
        for key in keys:
            if key == pygame.K_UP:
                self.rect.y -= self.spd
            elif key == pygame.K_DOWN:
                self.rect.y += self.spd
            elif key == pygame.K_RIGHT:
                if self.lr == -1:
                    self.lr = 1
                    self.frames = list(map(lambda x: pygame.transform.flip(x, 1, 0), self.frames))
                    self.image = self.frames[self.cur_frame]
                self.rect.x += self.spd

            elif key == pygame.K_LEFT:
                if self.lr == 1:
                    self.lr = -1
                    self.frames = list(map(lambda x: pygame.transform.flip(x, 1, 0), self.frames))
                    self.image = self.frames[self.cur_frame]
                self.rect.x -= self.spd