import pygame
from copy import deepcopy

STARTING_MAP = [
       [0, 0, 1, 1, 1, 0, 0],
       [0, 0, 1, 1, 1, 0, 0],
       [1, 1, 1, 1, 1, 1, 1],
       [1, 1, 1, 2, 1, 1, 1],
       [1, 1, 1, 1, 1, 1, 1],
       [0, 0, 1, 1, 1, 0, 0],
       [0, 0, 1, 1, 1, 0, 0]]

actual_map = []
all_balls = []
all_empty_balls = []

pygame.init()

RESOLUTION = (len(STARTING_MAP) * 50, len(STARTING_MAP[0]) *50)
game_display = pygame.display.set_mode(RESOLUTION)

BALL = pygame.image.load('ball.png').convert_alpha()
BALL_CIEN = pygame.image.load('ball_cien.png').convert_alpha()
BALL_RECT = BALL.get_rect()


class Mouse:
    ball = None
    ball_cords = None
    def grab_ball(self, ball):

        self.initiall = ball
        self.initiall_cords = grid.get_cords(ball)
        self.ball = ball

    def set_ball(self):
        ball_cords = grid.get_cords(self.ball)
        if grid.place(self.initiall_cords, ball_cords):
            self.move()
            all_balls.remove(self.ball)
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
                print('offset',offset)
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
            new_ball = BALL.get_rect()
            new_ball = new_ball.move(x * BALL_RECT.width, y * BALL_RECT.height)
            all_empty_balls.append(deepcopy(new_ball))  # NO TUTAJ SIĘ * zaczy poirytowałęm
            if is_ball == 1:
                all_balls.append(new_ball)  # NO TUTAJ SIĘ * zaczy poirytowałęm

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

                mouse.set_ball()
            elif not mouse.ball and ball_clicked:
                mouse.grab_ball(ball_clicked[0])

    if mouse.ball:
        mouse.move()

    game_display.fill((255, 255, 255))

    for empty_space in all_empty_balls:
        game_display.blit(BALL_CIEN, empty_space)

    for ball in all_balls:
        game_display.blit(BALL, ball)

    if mouse.ball:
        game_display.blit(BALL, mouse.ball)
    pygame.display.update()