from map import load_level, Map
from entities import AnimatedSprite
from our_tools import load_image, all_sprites
from start_screen import *
import pygame
from game_over import game_over
from tiles import tiles_group

pygame.init()

FPS = 60
clock = pygame.time.Clock()

man = AnimatedSprite(load_image("ninja_walking.png"), 4, 4, 64, 64)
direct = []
running = True
username = start_screen()
score = 5000

# Карта
level_map = [list(el) for el in load_level('map.map')]
mape = Map(level_map)
hero, level_x, level_y = mape.generate_level()

# экран
screen = pygame.display.set_mode(mape.size)
level_name = 'level 0'
pygame.display.set_caption(level_name)

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

# Вызов экрана конца игры. Теперь никнейм берётся из стартскрина, а очки в переменной score.
pygame.display.set_mode((800, 500))
game_over(username, score)
pygame.quit()
