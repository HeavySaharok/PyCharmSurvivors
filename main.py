from entities import AnimatedSprite
from our_tools import load_image, all_sprites
from start_screen import *
import os
import pygame
from game_over import game_over

pygame.init()

FPS = 60
WIDTH = 600
HEIGHT = 600
clock = pygame.time.Clock()

man = AnimatedSprite(load_image("man_1.png"), 8, 1, 150, 150)
direct = []
running = True
username = start_screen()
score = 5000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

# Вызов экрана конца игры. Теперь никнейм берётся из стартскрина, а очки в переменной score.
pygame.display.set_mode((800, 500))
game_over(username, score)
pygame.quit()
