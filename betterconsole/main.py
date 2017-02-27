import pygame
import configparser
import subprocess
import time
import shlex

def execute(cmd):
    cmd = shlex.split(cmd)
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line

    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

conf = configparser.ConfigParser()
conf.read('config.txt')

COMMAND = conf['APP']['command']
#GRID = (int(conf['APP']['num_columns']),int(conf['APP']['num_rows']))
NAME = conf['APP']['name']
SHOW_FPS = conf['APP']['show_fps'].lower()
MAX_FPS = int(conf['APP']['fps'])
BLOCK = (int(conf['BLOCK']['width']), int(conf['BLOCK']['height']))
COLORS = {}

for rule, value in conf['COLORS'].items():
    values = value[1:-1].split(",")
    COLORS[rule.lower()] = [int(val.strip()) for val in values]


print(COMMAND, BLOCK, COLORS)

pygame.init()
pygame.display.set_caption(NAME)
screen = pygame.display.set_mode((BLOCK[0], BLOCK[1]))

my_font = pygame.font.Font(pygame.font.get_default_font(),23)

clock = pygame.time.Clock()
screen_width = 0
screen_height = 0
y = 0
fps = 0
last_fps_surface = (0,0,0,0)
for output_line in execute(COMMAND):

    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    except KeyboardInterrupt:
        pygame.quit()
        quit()

    output_line = list(output_line)
    #print(output_line, y)
    if len(output_line) == 1:
        #print('Something is wrong')
        # if y != GRID[1]:
        #     #print(y, GRID[1])
        #     raise Exception('WrongRows')
        y = 0
        continue
    # elif len(output_line) - 1 != GRID[0]:
    #     raise Exception('WrongColumns')
    for x,char in enumerate(output_line[0:-1]):
        try:
            char = char.lower()
        except AttributeError:
            char = char
        if x + 1 > screen_width or y > screen_height:
            if x + 1 > screen_width:
                screen_width = x + 1
            if y > screen_height:
                screen_height = y + 1
            screen = pygame.display.set_mode((screen_width * BLOCK[0],
                                             screen_height * BLOCK[1]))
        pygame.draw.rect(screen, COLORS[char],(x * BLOCK[0],
                                               y * BLOCK[1],
                                               BLOCK[0],
                                               BLOCK[1]))



    clock.tick(MAX_FPS * screen_height)

    if SHOW_FPS == 'true':
        try:
            fps = clock.get_fps()/ screen_height
        except ZeroDivisionError:
            fps = 1

        surface = my_font.render(str(fps//1), True, (0, 255, 0))

        pygame.draw.rect(screen, (0,0,0),last_fps_surface)

        screen.blit(surface, (0, 0))
        last_fps_surface = surface.get_rect()
    pygame.display.update()




    y += 1























        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         quit()
        # screen.draw()
        #
        #
        # screen.update()