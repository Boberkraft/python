import copy
import time

class Game_of_life():
    def __init__(self, x, y):
        self.x_size = x
        self.y_size = y
        self.area = [['.' for px in range(y)] for py in range(x)]
        self.new_area = [['.' for px in range(y)] for py in range(x)]

    def get_area(self):
        return self.area

    def set_cells(self, x, y):
        if self.area[x][y] == '#':
            self.area[x][y] = '.'
            print('dead')
        elif self.area[x][y] == '.':
            self.area[x][y] = '#'
            print('live')

    def check_cells(self):

        self.new_area = copy.deepcopy(self.area)

        for x_index, x in enumerate(self.area):
            for y_index, y in enumerate(x):

                if x_index == 0 or x_index == len(self.area) - 1:
                    continue
                elif y_index == 0 or y_index == len(x) - 1:
                    continue

                # print("At",x_index,y_index)
                nerbly = 0
                for x_c in range(-1, 2):
                    for y_c in range(-1, 2):
                        new_x = x_index + x_c
                        new_y = y_index + y_c
                        # print(new_x, new_y)
                        if x_c == 0 and y_c == 0:
                            continue

                        if self.area[new_x][new_y] == '#':
                            nerbly += 1
                if self.area[x_index][y_index] == '#':
                    # print('Its a cell',nerbly)
                    if nerbly < 2:
                        self.new_area[x_index][y_index] = '.'
                        # print('Im alone')
                    elif nerbly >= 4:
                        self.new_area[x_index][y_index] = '.'
                        # print('To many cells')
                    else:
                        self.new_area[x_index][y_index] = '#'
                        #print('im ok')

                if nerbly == 3 and self.area[x_index][y_index] == '.':
                    self.new_area[x_index][y_index] = '#'
                    #print('I should spawn', nerbly)

        self.area = self.new_area[:]


def draw(area):
    for x in area:
        for y in x:
            print(y, end='')
        print()


def main():
    Game = Game_of_life(10, 30)
    Game.set_cells()
    area = Game.get_area()
    while 1:
        draw(area)
        Game.check_cells()
        time.sleep(0.1)
        area = Game.get_area()
        os.system("cls")

if __name__ == '__main_':
    main()
