import sys
import pygame
from database import Database
pygame.init()


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
    unique = 0
    size = 230, 360
    screen = pygame.display.set_mode(size)
    screen.fill('white')
    pygame.display.set_caption('Results')
    players = Database('players.sqlite')
    result_text = [('#   ', 'Имя         ', 'Счёт')]
    lis = sorted(players.get_val('scores', '*', '')[:10], key=lambda x: x[2], reverse=True)
    for i in range(len(lis)):
        _, name, score = lis[i]
        if name == player_name:
            unique = i
        if len(name) > 10:
            name = name[:7] + '...'
        result_text.append((str(i + 1), name, str(score)))

    font = pygame.font.Font(None, 30)
    text_coord = 30
    for i in range(len(result_text)):
        place, name, score = result_text[i]
        if i - 1 == unique:
            p_rendered = font.render(place, 1, pygame.Color('Red'))
            n_rendered = font.render(name, 1, pygame.Color('Red'))
            s_rendered = font.render(score, 1, pygame.Color('Red'))
        else:
            p_rendered = font.render(place, 1, pygame.Color('Black'))
            n_rendered = font.render(name, 1, pygame.Color('Black'))
            s_rendered = font.render(score, 1, pygame.Color('Black'))

        p_rect, n_rect, s_rect = p_rendered.get_rect(), n_rendered.get_rect(), s_rendered.get_rect()
        text_coord += 10
        p_rect.top, n_rect.top, s_rect.top = [text_coord] * 3
        p_rect.x, n_rect.x, s_rect.x = 10, 35, 135
        text_coord += p_rect.height
        screen.blit(p_rendered, p_rect)
        screen.blit(n_rendered, n_rect)
        screen.blit(s_rendered, s_rect)
    pygame.draw.line(screen, 'Black', (0, 30), (0, 360), 3)
    pygame.draw.line(screen, 'Black', (30, 30), (30, 360), 3)
    pygame.draw.line(screen, 'Black', (130, 30), (130, 360), 3)
    pygame.draw.line(screen, 'Black', (230, 30), (230, 360), 3)
    congrats = f'Вы знаяли {unique + 1} место!!!'
    cong_ot = font.render(congrats, 1, pygame.Color('Red'))
    cong_rec = cong_ot.get_rect()
    cong_rec.y = 5
    cong_rec.x = (230 - cong_rec.width) // 2
    screen.blit(cong_ot, cong_rec)
    for j in range(12):
        pygame.draw.line(screen, 'Black', (0, 30 * j + 30), (230, 30 * j + 30), 3)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()


if __name__ == '__main__':
    result_screen('Eva')
