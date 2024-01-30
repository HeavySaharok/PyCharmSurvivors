import sys
import pygame


class Levels:
    # создание кнопок
    def __init__(self, width, height, username):
        self.height = height
        self.width = width
        self.username = username
        # значения по умолчанию
        self.left = 55
        self.top = 300
        self.cell_size = 85
        self.rects = []

    def render(self, screen):
        # pygame.draw.rect(screen, pygame.Color(0, 0, 0), (self.left, self.top, self.cell_size, self.cell_size - 100), 3)
        # font = pygame.font.Font(None, 25)
        # screen.blit(font.render('НАЧАТЬ ИГРУ', True, pygame.Color('black')),
        #             (self.left + 15, self.top + 15, self.cell_size, self.cell_size))
        c = 0
        for y in range(1, self.width + 1):
            for x in range(self.height):
                c += 1
                font = pygame.font.Font(None, 40)
                screen.blit(font.render(str(c) + '.lvl', True, pygame.Color(123, 104, 238)),
                           (x * self.cell_size * 1.45 + 68,
                            (y - 1) * self.cell_size + self.top + 45, self.cell_size, self.cell_size))
                rect = pygame.draw.rect(screen, pygame.Color(0, 255, 0), (
                    x * self.cell_size * 1.45 + 50, (y - 1) * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 3)
                if len(self.rects) < self.width * self.height:
                    self.rects.append([rect.topleft, rect.topright, rect.bottomleft])



    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
    def get_cell(self, mouse_pos):
        '''дописать
        '''
        num_lvl = 0
        # print(len(self.rects))
        # print(mouse_pos)
        for i in range(len(self.rects)):

            # print(self.rects[i][0][0], self.rects[i][1][0], self.rects[i][0][1], self.rects[i][2][1])
            if (self.rects[i][0][0] <= mouse_pos[0] <= self.rects[i][1][0]) and (self.rects[i][0][1] <= mouse_pos[1] <= self.rects[i][2][1]):
                num_lvl = i + 1

        return num_lvl

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            print(f'now level = {cell}, username = {self.username}')
            return (cell), self.username
    # # def get_click(self, mouse_pos):
    #     x = mouse_pos[0]
    #     y = mouse_pos[1]
    #     if self.left < x < (self.left + self.cell_size) and self.top < y < (self.top + self.cell_size - 100):
    #         print(self.username)
    #         return self.username

        #     вызов игрового окна

        # cell = self.get_cell(mouse_pos)
        # if cell:
        #     print(f'now level = {sum(cell)}, username = {self.username}')
        #     return sum(cell), self.username


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(lvl, username):
    """
    Вызвать из начала игры один раз:
    :return: username
    """
    screen.fill(pygame.Color('white'))
    intro_text = ["", "",
                  "Введите Ваше имя:", "",
                  "собирайте двоичные числа,",
                  f"ВЫБЕРИТЕ УРОВЕНЬ: до {lvl}"]
    fon = pygame.image.load('data/logo-2.png')
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 36)
    text_coord = 60
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 80
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    base_font = pygame.font.Font(None, 32)
    user_text = username

    input_rect = pygame.Rect(80, 170, 140, 32)
    color_active = pygame.Color("#3CB371")

    color_passive = pygame.Color("#006400")
    active = False

    # pygame.draw.rect(screen, pygame.Color(0, 0, 0), (480, 200, 150, 50), 3)
    # font = pygame.font.Font(None, 25)
    # screen.blit(font.render('НАЧАТЬ ИГРУ', True, pygame.Color('black')), (495, 215, 90, 90))

    levels = Levels(lvl // 3, lvl // (lvl // 3), username)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = levels.get_click(event.pos)
                if click is None:
                    pass
                else:
                    pygame.quit()
                    return click

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
                levels.username = user_text

        if active:
            color = color_active
        else:
            color = color_passive

        pygame.draw.rect(screen, color, input_rect)
        text_surface = base_font.render(user_text, True, "black")

        # рендеринг согласно вводу мени пользователя
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = max(100, text_surface.get_width() + 10)

        levels.render(screen)
        pygame.display.flip()


ll = 15
WIDTH, HEIGHT = size = 640, 900
print(HEIGHT)
pygame.init()
FPS = 50
screen = pygame.display.set_mode(size)
pygame.display.set_caption('PyCharm Survivors')

if __name__ == '__main__':
    start_screen(ll, '')
