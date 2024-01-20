from map import load_level, Map
from start_screen import *
import os
import pygame
from tiles import tiles_group

pygame.init()

FPS = 60
WIDTH = 600
HEIGHT = 600
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()


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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.times = 0
        self.spd = 2
        self.frames = []
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
        global lr
        for key in keys:
            if key == pygame.K_UP:
                self.rect.y -= self.spd
            elif key == pygame.K_DOWN:
                self.rect.y += self.spd
            elif key == pygame.K_RIGHT:
                if lr == -1:
                    lr = 1
                    self.frames = list(map(lambda x: pygame.transform.flip(x, 1, 0), self.frames))
                    self.image = self.frames[self.cur_frame]
                self.rect.x += self.spd

            elif key == pygame.K_LEFT:
                if lr == 1:
                    lr = -1
                    self.frames = list(map(lambda x: pygame.transform.flip(x, 1, 0), self.frames))
                    self.image = self.frames[self.cur_frame]
                self.rect.x -= self.spd


man = AnimatedSprite(load_image("man_1.png"), 8, 1, 150, 150)
direct = []
lr = 1
running = True
start_screen()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Карта
level_map = [list(el) for el in load_level('map.map')]
mape = Map(level_map)
hero, level_x, level_y = mape.generate_level()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            direct.append(event.key)
            print(direct)
        if event.type == pygame.KEYUP and event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            direct.pop(direct.index(event.key))

    screen.fill(pygame.Color("black"))
    if direct:
        all_sprites.update()
        man.move(direct)
    tiles_group.draw(screen)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
