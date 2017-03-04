import pygame
from copy import deepcopy
from enum import IntEnum


# it works so whats the problem XD?
# now lets work on commenting this one, and refactor map drawing
# TODO sound

STARTING_MAP = [
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 1, 1, 1, 0, 0, 0],
       [0, 0, 0, 1, 1, 1, 0, 0, 0],
       [0, 1, 1, 1, 1, 1, 1, 1, 0],
       [0, 1, 1, 1, 2, 1, 1, 1, 0],
       [0, 1, 1, 1, 1, 1, 1, 1, 0],
       [0, 0, 0, 1, 1, 1, 0, 0, 0],
       [0, 0, 0, 1, 1, 1, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],]

actual_map = []
all_balls = []
all_empty_balls = []

pygame.init()

RESOLUTION = (len(STARTING_MAP[0]) * 50, len(STARTING_MAP) * 50)
game_display = pygame.display.set_mode(RESOLUTION)

BALL_SHADOW = pygame.image.load('img/ball_shadow.png').convert_alpha()
NO_BALL = pygame.image.load('img/no_ball.png').convert_alpha()
BALL = pygame.image.load('img/ball.png').convert_alpha()
BALL_RECT = BALL_SHADOW.get_rect()


BORDER_SHADOW = pygame.image.load('img/border_shadow.png').convert_alpha()
BORDER_LIGHT = pygame.image.load('img/border_light.png').convert_alpha()


class Level(IntEnum):
    Normal, Hard, Hardcore = range(3)

# oh god

def draw_background(map_to_render):

    def draw_on_left(x, y):
        surf = pygame.transform.rotate(BORDER_SHADOW, 90)
        rect = surf.get_rect()
        rect.x, rect.y = x, y
        game_display.blit(surf, rect)

    def draw_on_right(x, y):

        surf = pygame.transform.rotate(BORDER_LIGHT, 90)
        rect = surf.get_rect()
        rect.x, rect.y = x + BALL_RECT.width, y
        game_display.blit(surf, rect)

    def draw_on_top(x, y):

        surf = BORDER_SHADOW
        rect = surf.get_rect()
        rect.x, rect.y = x, y
        game_display.blit(surf, rect)

    def draw_on_bottom(x, y):

        surf = BORDER_LIGHT
        rect = surf.get_rect()
        rect.x, rect.y = x, y + BALL_RECT.height
        game_display.blit(surf, rect)

    for y, row in enumerate(map_to_render):
        for x, is_ball in enumerate(row):
            if is_ball == 0:
                try:
                    if map_to_render[y][x - 1] != 0:
                        draw_on_left(x * BALL_RECT.width, y * BALL_RECT.height)
                except IndexError: pass
                try:
                    if map_to_render[y][x + 1] != 0:
                        draw_on_right(x * BALL_RECT.width, y * BALL_RECT.height)
                except IndexError: pass
                try:
                    if map_to_render[y - 1][x] != 0:
                        draw_on_top(x * BALL_RECT.width, y * BALL_RECT.height)
                except IndexError: pass
                try:
                    if map_to_render[y + 1][x] != 0:
                        draw_on_bottom(x * BALL_RECT.width, y * BALL_RECT.height)
                except IndexError: pass
# end of oh god


class SoundManager:
    def __init__(self, lvl):
        self.lvl = lvl

    def play_background(self):
        pygame.mixer.music.load('music/%s.background.mp3' % self.lvl)
        pygame.mixer.music.play()

    def play_sound(self):
        effect = pygame.mixer.Sound('sound/%s.move.mp3' % self.lvl)
        effect.play()



class Mouse:
    ball = None
    ball_cords = None
    def grab_ball(self, ball):

        self.initiall = ball
        self.initiall_cords = grid.get_cords(ball)
        self.ball = ball
        all_balls.remove(self.ball)

    def set_ball(self):
        ball_cords = grid.get_cords(self.ball)
        if grid.place(self.initiall_cords, ball_cords):
            self.move()
            self.ball = None

    def move(self):
        pos = pygame.mouse.get_pos()
        self.ball.center = pos[0], pos[1]


class Grid:
    def __init__(self, map_arena):
        self.map_arena = map_arena

    def check(self, who, where):
        x = abs(who[0] - where[0])
        y = abs(who[1] - where[1])

        if max(x, y) == 2:
            if min(x, y) == 0:
                return True
        return False
        # return any([abs(x - y) == 2 or abs(x - y) == 0 for x, y in zip(who, where)])

    def remove(self, where):

        pos = self.get_pos(where)

        [all_balls.remove(ball) for ball in all_balls if ball.collidepoint(pos[0], pos[1]) if ball != mouse.ball]

    def place(self, who, where):

        if who == where:
            self.make_ball(where)

            return True
        if self.map_arena[where[0]][where[1]] == 2:
            if self.check(who, where):
                offset = ((who[0] - where[0]) // 2, (who[1] - where[1]) // 2)
                ball_between = (where[0] + offset[0],  where[1] + offset[1])
                if self.map_arena[ball_between[0]][ball_between[1]] == 1:
                    self.remove(ball_between)
                    self.map_arena[ball_between[0]][ball_between[1]] = 2
                    self.map_arena[who[0]][who[1]] = 2
                    self.map_arena[where[0]][where[1]] = 1
                    self.make_ball(where)
                    return True
        return False

    @staticmethod
    def make_ball(where):

        pos = pygame.Rect(where[0] * BALL_RECT.height, where[1] * BALL_RECT.width, BALL_RECT.width, BALL_RECT.height)

        all_balls.append(pos)

    # @staticmethod
    # def make_empty_space( where):
    #     print('making new space')
    #     pos = pygame.Rect(where[0] * BALL_RECT.width, where[1] * BALL_RECT.width, BALL_RECT.width, BALL_RECT.height)
    #     all_empty_balls.append(pos)

    @staticmethod
    def get_cords(who):
        return int(round(who.x / BALL_RECT.width)), int(round(who.y / BALL_RECT.height))

    @staticmethod
    def get_pos(who):
        return who[0] * BALL_RECT.width, who[1] * BALL_RECT.height

font = pygame.font.Font(None, 25)
BLACK = (0, 0, 0)
RED = (255,0,0)

class Menu:
    class Button:
        def __init__(self, name, caption, rect):
            self.name = name
            self.text = font.render(caption, True, BLACK)
            self.text_rect = self.text.get_rect(center=rect.center)
            self.rect = rect

    def __init__(self):
        self.all_buttons = []
        self.num_buttons = 0
        self.map_arena = []
        self.map_arena.append([0] * len(STARTING_MAP[0]))

    def add_button(self, name, caption):
        # render in the middle of screen
        new_button_rect = pygame.Rect((3 * BALL_RECT.width,
                            (len(self.map_arena)) * BALL_RECT.height),
                           ((len(STARTING_MAP[0]) - 6) * BALL_RECT.width,
                           BALL_RECT.width))

        self.all_buttons.append(Menu.Button(name, caption, new_button_rect))
        self.num_buttons += 1

        new_row = [0 if abs(index - len(STARTING_MAP)//2) > 1 else 1 for index, y in enumerate(STARTING_MAP)]
        self.map_arena.append(new_row)
        self.map_arena.append([0] * len(STARTING_MAP[0]))



menu = Menu()

class Overlay:
    def __init__(self, alpha, color):
        self.alpha = alpha
        self.color = color
    def draw(self):
        s = pygame.Surface(RESOLUTION)
        s.set_alpha(self.alpha)
        s.fill(self.color)
        game_display.blit(s, (0, 0))


for name, member in Level.__members__.items():
    menu.add_button(member, name)

mouse = Mouse()
game_level = Level.Normal
overlay = None
is_paused = True

def setup():
    global grid, tries, all_balls, all_empty_balls, is_paused, overlay
    is_paused = False
    all_balls = []
    all_empty_balls = []

    grid = Grid(STARTING_MAP)
    tries = 0
    for x, row in enumerate(STARTING_MAP):
        for y, is_ball in enumerate(row):
            if is_ball:
                new_ball = BALL_SHADOW.get_rect()
                new_ball = new_ball.move(x * BALL_RECT.width, y * BALL_RECT.height)
                all_empty_balls.append(deepcopy(new_ball))  # NO TUTAJ SIĘ poirytowałęm
                if is_ball == 1:
                    all_balls.append(new_ball)  # NO TUTAJ SIĘ poirytowałęm
    sound_manager = SoundManager(game_level)
    sound_manager.play_background()

    overlay = Overlay(game_level * 25, RED)



while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if not is_paused:
                ball_clicked = [ball for ball in all_balls if ball.collidepoint(x, y)]
                empty_space_clicked = [empty_space for empty_space in all_empty_balls if empty_space.collidepoint(x, y)]
                if mouse.ball and empty_space_clicked:
                    tries += 1
                    print('Number of click:', tries)
                    mouse.set_ball()
                elif not mouse.ball and ball_clicked:
                    mouse.grab_ball(ball_clicked[0])
            else:
                button_clicked = [button for button in menu.all_buttons if button.rect.collidepoint(x, y)]
                if len(button_clicked) > 0:
                    button_clicked = button_clicked[0]
                    if button_clicked.name in Level:
                        game_level = button_clicked.name
                        setup()


    if not is_paused:
        if mouse.ball:
            mouse.move()

        game_display.fill((200, 200, 200))

        draw_background(grid.map_arena)

        for empty_space in all_empty_balls:
            game_display.blit(NO_BALL, empty_space)

        for ball in all_balls:
            game_display.blit(BALL_SHADOW, ball)



        if mouse.ball:
            game_display.blit(BALL, mouse.ball)

        overlay.draw()
    else:
        game_display.fill((200, 200, 200))
        draw_background(menu.map_arena)
        for button in menu.all_buttons:
            game_display.blit(button.text, button.text_rect)
    pygame.display.update()
