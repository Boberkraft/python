import pygame
from copy import deepcopy
from enum import IntEnum

# author Andrzej Bisewski
# andrzej.bisewski@gmail.com
# just credit me


class Ball:
    sprite = None
    sprite_shadow = None

    def __init__(self, rect):
        self.rect = rect

    @classmethod
    def set_sprite(cls, what_level):
        # with more sprites i would chose one randomly from folder, but i don's soo..
        cls.sprite = pygame.image.load('img/%s.ball.png' % what_level).convert_alpha()
        cls.sprite_shadow = pygame.image.load('img/%s.ball_shadow.png' % what_level).convert_alpha()


class Level(IntEnum):
    Normal, Hard, Hardcore = range(3)


def draw_background(map_to_render):
    # oh god
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
                    if map_to_render[y][x - 1] != 0 and x - 1 >= 0:
                        draw_on_left(x * BALL_RECT.width, y * BALL_RECT.height)
                except IndexError: pass
                try:
                    if map_to_render[y][x + 1] != 0:
                        draw_on_right(x * BALL_RECT.width, y * BALL_RECT.height)
                except IndexError: pass
                try:
                    if map_to_render[y - 1][x] != 0 and y - 1 >= 0:
                        draw_on_top(x * BALL_RECT.width, y * BALL_RECT.height)
                except IndexError: pass
                try:
                    if map_to_render[y + 1][x] != 0:
                        draw_on_bottom(x * BALL_RECT.width, y * BALL_RECT.height)
                except IndexError: pass
    # end of oh god


class SoundManager:
    lvl = None

    @classmethod
    def set_level(cls, lvl):
        cls.lvl = lvl

    @classmethod
    def play_background(cls):
        pygame.mixer.music.load('music/%s.background.mp3' % cls.lvl)
        pygame.mixer.music.set_volume(0.10)
        pygame.mixer.music.play(-1)

    @classmethod
    def play_sound(cls):
        effect = pygame.mixer.Sound('sound/%s.move.wav' % cls.lvl)
        effect.play()


class Mouse:
    ball = None
    ball_cords = None

    def __init__(self):
        self.initial = None
        self.initial_cords = None

    def grab_ball(self, ball):
        self.initial = ball
        self.initial_cords = grid.get_cords(ball)
        self.ball = ball
        all_balls.remove(self.ball)

    def set_ball(self):
        ball_cords = grid.get_cords(self.ball)
        if grid.place(self.initial_cords, ball_cords):
            self.move()
            self.ball = None
            return True
        return False

    def move(self):
        pos = pygame.mouse.get_pos()
        self.ball.center = pos[0], pos[1]


class Grid:
    def __init__(self, map_arena):
        self.map_arena = deepcopy(map_arena)

    def check(self, who, where):
        x = abs(who[1] - where[1])
        y = abs(who[0] - where[0])

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
        if self.map_arena[where[1]][where[0]] == 2:
            if self.check(who, where):
                offset = ((who[1] - where[1]) // 2, (who[0] - where[0]) // 2)
                ball_between = (where[0] + offset[1],  where[1] + offset[0])
                if self.map_arena[ball_between[1]][ball_between[0]] == 1:
                    self.remove(ball_between)
                    self.map_arena[ball_between[1]][ball_between[0]] = 2
                    self.map_arena[who[1]][who[0]] = 2
                    self.map_arena[where[1]][where[0]] = 1
                    self.make_ball(where)
                    return True
        return False

    @staticmethod
    def make_ball(where):
        pos = pygame.Rect(where[0] * BALL_RECT.height, where[1] * BALL_RECT.width, BALL_RECT.width, BALL_RECT.height)
        all_balls.append(pos)

    @staticmethod
    def get_cords(who):
        return int(round(who.x / BALL_RECT.width)), int(round(who.y / BALL_RECT.height))

    @staticmethod
    def get_pos(who):
        return who[0] * BALL_RECT.width, who[1] * BALL_RECT.height


class Menu:
    class Button:
        def __init__(self, name, caption, rect,):
            self.name = name
            self.text = None
            self.caption = caption
            self.text_rect = None
            self.rect = rect
            self.text_rect = rect

        def set_text(self):
            self.text = font.render(self.caption, True, (97 * self.name,97,97))
            self.text_rect = self.text.get_rect(center=self.rect.center)

    def __init__(self):
        self.all_buttons = []
        self.func_buttons = []
        self.map_arena = []
        self.map_arena.append([0] * len(STARTING_MAP[0]))

    def add_func_button(self, name, img):
        new_button_rect = pygame.Rect(len(self.func_buttons) * HOME_BUTTON.get_width()  * 1.5 + 10 ,
                                      10,
                                      HOME_BUTTON.get_width(),
                                      HOME_BUTTON.get_height())
        new_button = Menu.Button(name, 'you cant see this!', new_button_rect)
        new_button.text = img
        self.func_buttons.append(new_button)

    def add_button(self, name, caption):
        # render in the middle of screen
        new_button_rect = pygame.Rect((3 * BALL_RECT.width,  # x
                                       (len(self.map_arena)) * BALL_RECT.height),  # y
                                      ((len(STARTING_MAP[0]) - 6) * BALL_RECT.width,  # width
                                       BALL_RECT.width))  # height
        new_button = Menu.Button(name, caption, new_button_rect)
        new_button.set_text()
        self.all_buttons.append(new_button)


        new_row = [0 if abs(index - len(STARTING_MAP)//2) > 1 else 1 for index, y in enumerate(STARTING_MAP)]
        self.map_arena.append(new_row)
        self.map_arena.append([0] * len(STARTING_MAP[0]))


class Overlay:
    def __init__(self, alpha, color):
        self.alpha = alpha
        self.color = color

    def draw(self):
        s = pygame.Surface(RESOLUTION)
        s.set_alpha(self.alpha)
        s.fill(self.color)
        game_display.blit(s, (0, 0))  # renders on whole screen

# END OF CLASSES

# it works so whats the problem XD?
# now lets work on commenting this one, and refactoring map drawing (but how?)

# -------------------------------- ACTUAL START -------------------------------- #

# map that is loaded at start
STARTING_MAP = [
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 1, 1, 1, 0, 0, 0],
       [0, 0, 0, 1, 1, 1, 0, 0, 0],
       [0, 1, 1, 1, 1, 1, 1, 1, 0],
       [0, 1, 1, 1, 2, 1, 1, 1, 0],
       [0, 1, 1, 1, 1, 1, 1, 1, 0],
       [0, 0, 0, 1, 1, 1, 0, 0, 0],
       [0, 0, 0, 1, 1, 1, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0]]

# sets small buffer  so sound apear fast
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=256)
pygame.init()

RESOLUTION = (len(STARTING_MAP[0]) * 50, len(STARTING_MAP) * 50)
game_display = pygame.display.set_mode(RESOLUTION)

# default sprites
NO_BALL = pygame.image.load('img/no_ball.png').convert_alpha()
BALL = pygame.image.load('img/Level.Normal.ball.png').convert_alpha()
BALL_RECT = BALL.get_rect()

HOME_BUTTON = pygame.image.load('img/home.png').convert_alpha()
RETRY_BUTTON = pygame.image.load('img/retry.png').convert_alpha()

BORDER_SHADOW = pygame.image.load('img/border_shadow.png').convert_alpha()
BORDER_LIGHT = pygame.image.load('img/border_light.png').convert_alpha()

# font
font = pygame.font.Font('fonts/Vera-Bold.ttf', 25)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (200, 200, 200)
# END OF CONSTANTS

all_balls = []  # contains all ball sprites except that one in hand
all_empty_balls = []  # contains all empty spaces sprites for balls

game_level = None  # chosen level
overlay = None  # chosen overlay
tries = None  # number of tries
grid = None  # object containing actual grid
is_paused = True  # is main menu turned on?

menu = Menu()  # main menu
for name, member in Level.__members__.items():
    # adds buttons to main menu from list of available levels of hardness
    menu.add_button(member, name)
menu.add_func_button('home', HOME_BUTTON)
menu.add_func_button('retry', RETRY_BUTTON)
mouse = Mouse()   # mouse pointer that can hold one ball


def setup(replay_music=True):
    # the setup that starts the game
    global grid, tries, all_balls, all_empty_balls, is_paused, overlay
    is_paused = False
    all_balls = []
    all_empty_balls = []

    grid = Grid(STARTING_MAP)  # load this map
    tries = 0

    # determines what points on starting map are actually balls or holes
    for y, row in enumerate(STARTING_MAP):
        for x, is_ball in enumerate(row):
            if is_ball:
                new_ball_rect = BALL_RECT
                new_ball_rect = new_ball_rect.move(x * BALL_RECT.width, y * BALL_RECT.height)
                new_ball = Ball(new_ball_rect)
                all_empty_balls.append(new_ball.rect.copy())  # adds to list of holes
                if is_ball == 1:
                    all_balls.append(new_ball.rect)  # its a ball, so add to list of balls

    # setting sound
    if replay_music:
        SoundManager.set_level(game_level) # what theme it needs to play?
        SoundManager.play_background()

    # sets sprite for balls
    Ball.set_sprite(game_level)
    # setting overlay for whole map
    overlay = Overlay(game_level * 25, RED)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # you clicked quit
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # you clicked
            x, y = event.pos  # position of cursor
            if not is_paused:
                # the game is running!
                ball_clicked = [ball for ball in all_balls if ball.collidepoint(x, y)]
                empty_space_clicked = [empty_space for empty_space in all_empty_balls if empty_space.collidepoint(x, y)]

                if mouse.ball and empty_space_clicked:
                    # you have ball in hand and clicked empty space
                    if mouse.set_ball():  # tries to set a ball
                        SoundManager.play_sound()

                elif not mouse.ball and ball_clicked:
                    # you don't have ball in hand and clicked ball
                    ball_clicked = ball_clicked[0]
                    mouse.grab_ball(ball_clicked)  # grabs a ball

                button_clicked = [button for button in menu.func_buttons if button.rect.collidepoint(x, y)]
                if button_clicked:
                    # you clicked a button
                    button_clicked = button_clicked[0]
                    if button_clicked.name == 'home':
                        # you clicked a button with name same as one of available levels
                        is_paused = True

                    if button_clicked.name == 'retry':
                        setup(False)
            else:
                # you are in main menu :)
                button_clicked = [button for button in menu.all_buttons if button.rect.collidepoint(x, y)]
                if button_clicked:
                    # you clicked a button
                    button_clicked = button_clicked[0]
                    if button_clicked.name in Level:
                        # you clicked a button with name same as one of available levels
                        if game_level != button_clicked.name:
                            game_level = button_clicked.name  # sets new level of hardness
                            setup()  # restarts the game
                        else:
                            is_paused = False

    game_display.fill(GREY)  # default background color

    if not is_paused:
        # the game is running!
        if mouse.ball:
            # you are holding a ball, move it
            mouse.move()

        draw_background(grid.map_arena)  # draws contours of main map

        for empty_space in all_empty_balls:
            # draws all holes
            game_display.blit(NO_BALL, empty_space)


        for ball in all_balls:
            # draws all balls
            game_display.blit(Ball.sprite_shadow, ball)
            game_display.blit(Ball.sprite, ball)

        if mouse.ball:
            # you are holding a ball, show it!
            game_display.blit(Ball.sprite, mouse.ball)

        for button in menu.func_buttons:
            game_display.blit(button.text, button.text_rect)
        overlay.draw()  # makes the screen more red
    else:
        # you are in main menu :)
        draw_background(menu.map_arena)  # draws contours of main menu
        for button in menu.all_buttons:
            # draws all buttons
            game_display.blit(button.text, button.text_rect)

    pygame.display.update()  # updates screen
