import pygame
import math
from pygame.locals import *
import langton

RESOLUTION = (1000, 500)
GAME_GRID = (100, 50)
HOW_FAST = 1
WHITE = (255,255,255)
PURPLE = (135,95,154)
BLACK = (0,0,0)


class Game():

    def __init__(self, x, y):
        self.map = langton.Map(x, y)
        self.block_rect = (RESOLUTION[0]/x, RESOLUTION[1]/y)
        self.iterations = 0

    def setup(self):
        pygame.init()

        ant1 = langton.Ant(self.map.get_num_ants())
        self.map.add_ant(ant1, self.map.x//2 , self.map.y//2)
        self.GAME_END = False
        self.game_display = pygame.display.set_mode(RESOLUTION, RESIZABLE)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("WOJTEK CIOTA")

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.GAME_END = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event)
                mouse_x = int(event.pos[0] // self.block_rect[0])
                mouse_y = int(event.pos[1] // self.block_rect[1])
                print(mouse_x, mouse_y)
                self.map.add_ant(langton.Ant(self.map.get_num_ants()), mouse_x, mouse_y)


    def draw_area(self):
        self.block_rect = (RESOLUTION[0] / self.map.x, RESOLUTION[1] / self.map.y)
        for x, row in enumerate(self.map.get_area()):
            for y, col in enumerate(row):
                x_pos = self.block_rect[0] * x
                y_pos = self.block_rect[1] * y
                height = self.block_rect[1] + 1
                width = self.block_rect[0] + 1
                if col[0] == 0:
                    if len(col) > 1:
                        pass
                        pygame.draw.rect(self.game_display, (255,100,200), (x_pos, y_pos, height, width))
                    else:
                        pass
                    pygame.draw.rect(self.game_display, WHITE, (x_pos, y_pos, height, width))
                else:
                    random = (((math.sqrt(col[0]*2))**col[0])* 10)%255
                    random_color = ((random* col[0])%255, (random*20)%255, (random*random)%255)
                    pygame.draw.rect(self.game_display, BLACK, (x_pos, y_pos, height, width))

    def main_loop(self):
        self.event_loop()

        for iter in range(HOW_FAST):
            self.map.update_ants()

        self.game_display.fill(WHITE)

        self.iterations += 1
        self.draw_area()


        self.clock.tick(60)
        self.message(str(self.clock.get_fps()//1),0)
        self.message(str(self.iterations),1)

        pygame.display.update()


    def is_end(self):
        return self.GAME_END

    def quit(self):
        pygame.quit()

    def message(self, text, where):

        default_font = pygame.font.get_default_font()
        font = pygame.font.Font('freesansbold.ttf', 22)
        shifting = font.render('', False, BLACK).get_rect()[3] * where
        text_surface = font.render(text, True, BLACK)

        self.game_display.blit(text_surface, (0, shifting))




if __name__ == '__main__':

    game = Game(GAME_GRID[0],GAME_GRID[1])

    game.setup()
    while 1:
        game.main_loop()

        if game.is_end():
            break
    game.quit()