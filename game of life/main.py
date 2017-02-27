import pygame
from game_of_life import *

black = (0,0,0)
white = (255,255,255)
green = 0x42f489
grey = 0xe4fcd9
resolution = (500,500)
cell_resoluton = (50,50)
def draw_area(area):
    for x_num, cell_x in enumerate(area):
        for y_num, cell_y in enumerate(cell_x):
            if cell_y == '.':
                pygame.draw.rect(game_display, grey, ((x_num)*10,(y_num+1)*10,10,10))
            elif cell_y == '#':
                pygame.draw.rect(game_display, green, ((x_num) * 10, (y_num + 1) * 10, 10, 10))
def main_loop():
    global start

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = not start
        if event.type == pygame.MOUSEBUTTONDOWN:
            # print(event)
            cell_x, cell_y = (pos//10 for pos in event.pos)
            game.set_cells(cell_x, cell_y-1)


    game_display.fill(grey)

    draw_area(area)

    pygame.display.update()
    if start == True:
        game.check_cells()
        clock.tick(2)
    else:
        clock.tick(60)

def setup():
    pass

def end():
    pygame.quit()
    quit()


if __name__ == '__main__':
    print('Clock on area to spawn block, and space to start/stop')
    pygame.init()
    start = False
    game_display = pygame.display.set_mode(resolution)
    pygame.display.set_caption('Game of life')
    clock  = pygame.time.Clock()
    game = Game_of_life(cell_resoluton[0], cell_resoluton[1])
    area = game.get_area()


    GAME_END = False
    while not GAME_END:
        main_loop()
        area = game.get_area()
    end()

