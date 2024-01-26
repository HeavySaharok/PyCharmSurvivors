import sys
import pygame
from database import Database
from our_tools import load_image
cl = pygame.time.Clock()


def terminate():
    """
    Закрываем лавочку
    :return:
    """
    pygame.quit()
    sys.exit()


def result_screen(player_name: str):
    """
    Вызываем экран результатов
    :param player_name: имя текущего игрока
    :return:
    """
    pygame.init()
    unique = 0
    size = 800, 500
    screen = pygame.display.set_mode(size)
    screen.fill('white')
    pygame.display.set_caption('Results')
    players = Database('players.sqlite')
    result_text = [('#' + '   ' + 'Имя' + '          ' + 'Счёт')]
    lis = sorted(players.get_val('scores', '*', '')[:10], key=lambda x: x[2], reverse=True)
    for i in range(len(lis)):
        _, name, score = lis[i]
        if name == player_name:
            unique = i
        if len(name) > 10:
            name = name[:7] + '...'
        result_text.append(str(i + 1) + '   ' + name + ' ' * (10 - len(name)) + '   ' + str(score))

    font = pygame.font.Font(None, 30)
    text_coord = 0
    for i in range(len(result_text)):
        line = result_text[i]
        if i - 1 == unique:
            string_rendered = font.render(line, 1, pygame.Color('Red'))
        else:
            string_rendered = font.render(line, 1, pygame.Color('Black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.draw.line(screen, 'Black', (0, 0), (0, 330), 3)
    pygame.draw.line(screen, 'Black', (30, 0), (30, 330), 3)
    pygame.draw.line(screen, 'Black', (130, 0), (130, 330), 3)
    pygame.draw.line(screen, 'Black', (230, 0), (230, 330), 3)
    for j in range(12):
        pygame.draw.line(screen, 'Black', (0, 30 * j), (230, 30 * j), 3)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        cl.tick(60)


def level_cleared(score: int):
    """
    Выводит поздравление с прохождением уровня и показывает кол-во очков.
    :param score: кол-во очков ирока
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
                    return 1
                elif event.key == pygame.K_ESCAPE:
                    pass
                    return 0
        pygame.display.flip()
        cl.tick(60)


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
                    return 1
                elif event.key == pygame.K_ESCAPE:
                    return 0
        pygame.display.flip()
        cl.tick(60)
