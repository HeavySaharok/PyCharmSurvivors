import sys
import pygame


class Levels:
    # создание кнопок
    def __init__(self, username):
        self.username = username
        # значения по умолчанию
        self.left = 480
        self.top = 50
        self.cell_size = 150

    def render(self, screen):
        pygame.draw.rect(screen, pygame.Color(0, 0, 0), (self.left, self.top, self.cell_size, self.cell_size - 100), 3)
        font = pygame.font.Font(None, 25)
        screen.blit(font.render('НАЧАТЬ ИГРУ', True, pygame.Color('black')),
                    (self.left + 15, self.top + 15, self.cell_size, self.cell_size))

        # for y in range(self.height):
        #     for x in range(self.width):
        #         font = pygame.font.Font(None, 55)
        #         screen.blit(font.render(str(y) + '.lvl', True, pygame.Color('black')),
        #                     (x * self.cell_size + 5 + self.left,
        #                      y * self.cell_size + self.cell_size // 3 + self.top, self.cell_size, self.cell_size))
        #         pygame.draw.rect(screen, pygame.Color(255, 255, 255), (
        #             x * self.cell_size + self.left, y * self.cell_size + self.top - 50, self.cell_size,
        #             self.cell_size), 3)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_click(self, mouse_pos):
        x = mouse_pos[0]
        y = mouse_pos[1]
        if self.left < x < (self.left + self.cell_size) and self.top < y < (self.top + self.cell_size - 100):
            print(self.username)
            return self.username

        #     вызов игрового окна

        # cell = self.get_cell(mouse_pos)
        # if cell:
        #     print(f'now level = {sum(cell)}, username = {self.username}')
        #     return sum(cell), self.username


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    '''
    Вызвать из начала игры один раз:
    return: username
    '''
    intro_text = [" ", "",
                  "Введите Ваше имя:", "",
                  "побеждайте противников", ''
                                            "проходите уровни"
                  ]
    screen.fill(pygame.Color('black'))
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
    user_text = ''

    input_rect = pygame.Rect(80, 170, 140, 32)
    color_active = pygame.Color("#3CB371")

    color_passive = pygame.Color("#006400")
    active = False

    # pygame.draw.rect(screen, pygame.Color(0, 0, 0), (480, 200, 150, 50), 3)
    # font = pygame.font.Font(None, 25)
    # screen.blit(font.render('НАЧАТЬ ИГРУ', True, pygame.Color('black')), (495, 215, 90, 90))

    levels = Levels(user_text)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = levels.get_click(event.pos)
                if click is None:
                    pass
                else:
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
        clock.tick(FPS)


WIDTH, HEIGHT = size = 640, 400
pygame.init()
clock = pygame.time.Clock()
FPS = 50
screen = pygame.display.set_mode(size)
pygame.display.set_caption('PyCharm Survivors')

if __name__ == '__main__':
    start_screen()
