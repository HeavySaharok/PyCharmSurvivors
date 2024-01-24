from map import load_level, Map
from entities import entity_group, hero_group
from our_tools import all_sprites
from start_screen import *
from screens import *
from tiles import tiles_group, obstacle_group
from database import Database

pygame.init()

FPS = 60
clock = pygame.time.Clock()

direct = []
running = True
username = start_screen()
score = 5000
level_name = 'test.map'
lev_done = 0
hero, level_x, level_y, screen = None, None, None, None


# Карта
def show():
    global hero, level_x, level_y, screen
    level_map = [list(el) for el in load_level(level_name)]
    mape = Map(level_map)
    hero, level_x, level_y = mape.generate_level()

    # экран
    screen = pygame.display.set_mode(mape.size)
    pygame.display.set_caption(level_name)


show()
# основной цикл
while running:
    if lev_done:
        a = level_cleared(score)
        lev_done = 0
        if not a:
            running = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            direct.append(event.key)
            # print(direct)
        if event.type == pygame.KEYUP and event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            direct.pop(direct.index(event.key))

    screen.fill(pygame.Color("black"))
    if direct:
        hero.move(direct)
    else:
        hero.standing = 1
    all_sprites.update()
    if hero_group.update() == 1:
        print('1')
        a = game_over()
        if not a:
            running = 0
    tiles_group.draw(screen)
    obstacle_group.draw(screen)
    entity_group.draw(screen)
    hero_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

# Вызов экрана конца игры. Теперь никнейм берётся из стартскрина, а очки в переменной score.
players = Database('players.sqlite')
players.insert('scores', ('name', 'score'), (username, score))
players.close()
result_screen(username)
pygame.quit()
