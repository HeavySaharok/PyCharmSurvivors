import sys
import pygame
from our_tools import load_image
from database import Database

FPS = 50
pygame.init()
size = WIDTH, HEIGHT = 800, 500
# screen = pygame.display.set_mode(size)    если это вне функции или класса, то влияет на всю игру
# pygame.display.set_caption('Game over')   поэтому это нужно сувать в функцию
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def game_over(name, score):
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Game over')
    result_text = []
    players = Database('players.sqlite')
    players.insert('scores', ('name', 'score'), (name, score))
    for elem in sorted(players.get_val('scores', '*', ''), key=lambda x: x[2], reverse=True):
        result_text.append(' '.join(list(map(str, elem))))
    fon = pygame.transform.scale(load_image('gmov.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 150
    for line in result_text:
        string_rendered = font.render(line, 1, pygame.Color('Blue'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 250
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    game_over('Vasya', 1421)
