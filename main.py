import pygame.time

from entities import entity_group
from map import load_level, Map
from our_tools import all_sprites
from screens import *
from start_screen import start_screen
from tiles import tiles_group, obstacle_group, finish_group, error_group

FPS = 60


direct = []
running = True
# присваивание уровня и имени пользователя
lv_id, username = start_screen(3, '')
score = 0
bounty = 5000
levels = ['1.map', '2.map', '3.map']
lev_done = 0


def clear_level():
    """
    Функция, чтобы очищать группы спрайтов и т.п.
    :return:
    """
    obstacle_group.empty()
    all_sprites.empty()
    entity_group.empty()
    tiles_group.empty()
    error_group.empty()
    finish_group.empty()


# Карта
def show(level_name):
    global bounty
    bounty = 5000
    pygame.init()
    # музыка
    pygame.mixer.music.load('data/Cello.ogg')
    pygame.mixer.music.play(-1)
    level_map = [list(el) for el in load_level(level_name)]
    mape = Map(level_map)
    # экран
    sc = pygame.display.set_mode(mape.size)
    pygame.display.set_caption(level_name)
    return mape.generate_level() + (sc, pygame.time.Clock())


hero, monsters, level_x, level_y, screen, clock = show(levels[lv_id])
# основной цикл
while running:
    if lev_done:
        pygame.quit()
        a = level_cleared(score)
        lev_done = 0
        if not a:
            running = 0
    screen.fill(pygame.Color("black"))
    if direct:
        hero.move(direct)
    else:
        hero.standing = 1
    for monster in monsters:
        monster.move()
    all_sprites.update()
    if hero.collis == 1:
        clear_level()
        pygame.quit()
        direct = []
        score = 0
        a = game_over()
        if not a:
            break
        else:
            hero, monsters, level_x, level_y, screen, clock = show(levels[lv_id])
            direct = []
    elif hero.collis == 2:
        clear_level()
        pygame.quit()
        direct = []
        score += int(bounty)
        a = level_cleared(score)
        if not a:
            break
        else:
            lv_id += 1
            if lv_id == len(levels):
                break
            else:
                pygame.quit()
                hero, monsters, level_x, level_y, screen, clock = show(levels[lv_id])
    tiles_group.draw(screen)
    obstacle_group.draw(screen)
    entity_group.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            direct.append(event.key)
        if event.type == pygame.KEYUP and event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            direct.pop(direct.index(event.key))
    clock.tick(FPS)
    bounty -= 1
    pygame.display.flip()

# Вызов экрана конца игры. Теперь никнейм берётся из стартскрина, а очки в переменной score.
pygame.quit()
if username != '':
    players = Database('players.sqlite')
    players.update_score('scores', username, score)
    players.close()
    result_screen(username)
    pygame.quit()