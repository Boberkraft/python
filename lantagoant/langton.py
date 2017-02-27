from copy import deepcopy
import time

class Map():
    WHITE = 0

    area = [] #[[(block_color, ant object)]]
    update_area = [] #structure for working with ants
    num_ants = 0 #number of ants

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.area = [[[0] for y in range(y)] for x in range(x)]
        self.update_area = [[[0] for y in range(y)] for x in range(x)]

    def add_ant(self, ant, x, y):
        self.area[x][y].append(ant)
        self.num_ants += 1

    def update_ants(self):
        self.update_area = [[[0] for y in range(self.y)] for x in range(self.x)]
        for x, line in enumerate(self.area):
            for y, col in enumerate(line):

                color = col[0]
                self.update_area[x][y][0] = color
                for ant in col[1:]:
                    (new_x, new_y), new_color = ant.move(color)
                    self.update_area[x][y][0] = new_color
                    try:
                        self.update_area[x + new_x][y + new_y].append(ant)
                    except IndexError:
                        #kill the ant
                        pass


        self.area = deepcopy(self.update_area)


    def get_area(self):
        return self.area

    def get_num_ants(self):
        return self.num_ants

def draw_area(area):
    drawning = ''
    for x in area:
        for y in x:

            drawning += ' ' + str(y[0]) + ' '

        drawning += '\n'
    print(drawning)


class Ant(Map):
    UP, LEFT, DOWN, RIGHT = 0, 1, 2, 3


    def __init__(self, color):
        self.color = color + 1
        self.facing = self.LEFT
        last_facing = self.facing

    def translate(self, move):
        if move == Ant.UP: return (1, 0)
        elif move == Ant.LEFT: return (0, -1)
        elif move == Ant.RIGHT: return (0, 1)
        elif move == Ant.DOWN: return (-1, 0)

    def move(self, color):
        self.last_facing = self.facing
        if color == Map.WHITE:
            self.facing = (self.facing + 1) % 4

            return self.translate(self.facing) , self.color
        else:
            self.facing = (self.facing - 1) % 4
            return self.translate(self.facing), Map.WHITE

if __name__ == '__main__':
    iter = 0
    map = Map(10,10)
    ant1 = Ant(map.get_num_ants())
    map.add_ant(ant1,5 ,5)
    draw_area(map.get_area())


    while 1:
        print(iter)
        iter += 1
        map.update_ants()
        draw_area(map.get_area())
        time.sleep(0.0001)
