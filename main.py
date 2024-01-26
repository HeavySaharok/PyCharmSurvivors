from map import load_level, Map
from entities import entity_group
from our_tools import all_sprites
from start_screen import *
from screens import *
from tiles import tiles_group, obstacle_group
from database import Database

FPS = 60
clock = pygame.time.Clock()

direct = []
running = True
username = start_screen()
score = 5000
levels = ['test.map']
lv_id = 0
lev_done = 0


# Карта
def show(level_name):
    pygame.init()
    level_map = [list(el) for el in load_level(level_name)]
    mape = Map(level_map)
    # экран
    sc = pygame.display.set_mode(mape.size)
    pygame.display.set_caption(level_name)
    h, lx, ly = mape.generate_level()
    return h, lx, ly, sc


hero, level_x, level_y, screen = show(levels[lv_id])
# основной цикл
while running:
    print('1')
    if lev_done:
        a = level_cleared(score)
        lev_done = 0
        if not a:
            running = 0
    screen.fill(pygame.Color("black"))
    if direct:
        hero.move(direct)
    else:
        hero.standing = 1
    all_sprites.update()
    if hero.collis == 1:
        pygame.quit()
        all_sprites.empty()
        entity_group.empty()
        a = game_over()
        if not a:
            break
        else:
            pygame.quit()
            hero, level_x, level_y, screen = show(levels[lv_id])
            direct = []
    elif hero.collis == 2:
        pygame.quit()
        all_sprites.empty()
        entity_group.empty()
        a = level_cleared(score)
        if not a:
            break
        else:
            lv_id += 1
            if lv_id == len(levels):
                break
            else:
                pygame.quit()
                hero, level_x, level_y, screen = show(levels[lv_id])
    print('2')
    tiles_group.draw(screen)
    obstacle_group.draw(screen)
    entity_group.draw(screen)
    print('2.5')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            direct.append(event.key)
        if event.type == pygame.KEYUP and event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            direct.pop(direct.index(event.key))
    clock.tick(60)
    pygame.display.flip()
    print(2.6)
    print('3')

# Вызов экрана конца игры. Теперь никнейм берётся из стартскрина, а очки в переменной score.
players = Database('players.sqlite')
players.insert('scores', ('name', 'score'), (username, score))
players.close()
result_screen(username)
pygame.quit()
