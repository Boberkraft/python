import pygame
from copy import deepcopy


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

BALL_SHADOW = pygame.image.load('ball_shadow.png').convert_alpha()
NO_BALL = pygame.image.load('no_ball.png').convert_alpha()
BALL = pygame.image.load('ball.png').convert_alpha()
BALL_RECT = BALL_SHADOW.get_rect()


BORDER_SHADOW = pygame.image.load('border_shadow.png').convert_alpha()
BORDER_LIGHT = pygame.image.load('border_light.png').convert_alpha()

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


def draw_map():
    for y, row in enumerate(grid.map_arena):
        for x, is_ball in enumerate(row):
            if is_ball == 0:
                try:
                    if grid.map_arena[y][x - 1] != 0:
                        draw_on_left(x * BALL_RECT.width, y * BALL_RECT.height)
                except IndexError: pass
                try:
                    if grid.map_arena[y][x + 1] != 0:
                        draw_on_right(x * BALL_RECT.width, y * BALL_RECT.height)
                except IndexError: pass
                try:
                    if grid.map_arena[y - 1][x] != 0:
                        draw_on_top(x * BALL_RECT.width, y * BALL_RECT.height)
                except IndexError: pass
                try:
                    if grid.map_arena[y + 1][x] != 0:
                        draw_on_bottom(x * BALL_RECT.width, y * BALL_RECT.height)
                except IndexError: pass
# end of oh god

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

        pos = pygame.Rect(where[0] * BALL_RECT.width, where[1] * BALL_RECT.width, BALL_RECT.width, BALL_RECT.height)

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

mouse = Mouse()

grid = Grid(STARTING_MAP)

for y, row in enumerate(STARTING_MAP):
    for x, is_ball in enumerate(row):
        if is_ball:
            new_ball = BALL_SHADOW.get_rect()
            new_ball = new_ball.move(x * BALL_RECT.width, y * BALL_RECT.height)
            all_empty_balls.append(deepcopy(new_ball))  # NO TUTAJ SIĘ poirytowałęm
            if is_ball == 1:
                all_balls.append(new_ball)  # NO TUTAJ SIĘ poirytowałęm


tries = 0
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            ball_clicked = [ball for ball in all_balls if ball.collidepoint(x, y)]
            empty_space_clicked = [empty_space for empty_space in all_empty_balls if empty_space.collidepoint(x, y)]
            if mouse.ball and empty_space_clicked:
                tries += 1
                print('Number of moves:', tries)
                mouse.set_ball()
            elif not mouse.ball and ball_clicked:
                mouse.grab_ball(ball_clicked[0])

    if mouse.ball:
        mouse.move()

    game_display.fill((200, 200, 200))

    draw_map()

    for empty_space in all_empty_balls:
        game_display.blit(NO_BALL, empty_space)

    for ball in all_balls:
        game_display.blit(BALL_SHADOW, ball)

    if mouse.ball:
        game_display.blit(BALL, mouse.ball)

    pygame.display.update()
