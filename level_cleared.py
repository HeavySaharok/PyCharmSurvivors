import sys
import pygame
from our_tools import load_image, next_level
pygame.init()


def terminate():
    pygame.quit()
    sys.exit()


def level_cleared(score):
    respar = 128
    size = w, h = 800, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Congrats!')
    end_text = ['Уровень пройден! Нажмите ПРОБЕЛ что бы перейти на следующий,', 'или ESC если вы хотите закончить игру.']
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
                    # next_level()
                    return
                elif event.key == pygame.K_ESCAPE:
                    pass
                    # вызов экрана результатов
                    return
        pygame.display.flip()


if __name__ == '__main__':
    level_cleared(5000)
