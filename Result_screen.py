import sys
import pygame
from database import Database
pygame.init()


def terminate():
    '''
    Закрываем лавочку
    :return:
    '''
    pygame.quit()
    sys.exit()


def result_screen(player_name: str):
    '''
    Вызываем экран результатов
    :param player_name: имя текущего игрока
    :return:
    '''
    unique = 0
    size = 800, 500
    screen = pygame.display.set_mode(size)
    screen.fill('white')
    pygame.display.set_caption('Results')
    players = Database('players.sqlite')
    result_text = [('#   Имя          Счёт')]
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


if __name__ == '__main__':
    result_screen('Eva')
