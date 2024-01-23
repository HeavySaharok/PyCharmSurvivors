import sys
import pygame
from our_tools import load_image
pygame.init()


def terminate():
    pygame.quit()
    sys.exit()


def game_over():
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
                    pass
                    # позже функция начала уровня заново
                    return
                elif event.key == pygame.K_ESCAPE:
                    pass
                    # вызов экрана результатов
                    return
        pygame.display.flip()


if __name__ == '__main__':
    game_over()
