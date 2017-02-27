import pygame
from copy import deepcopy

# no ten kod akurat jest baaardzo brzydki
# i wciąż ma buga, ale to potem

class Car:
    def __init__(self, rec, vel, color):
        self.x = rec[0]
        self.y = rec[1]
        self.width = rec[2]
        self.height = rec[3]
        self.velocity = vel # constant speed
        self.color = color

        self.crashed = False
        self.crashed_check = False
        self.ghost_x = False
        self.ghost_y = False
        self.clone = False

        # only for parents
        self.clones = []
        self.parent = self

    def move(self):
        # states in last frame
        last_ghost_x = self.ghost_x
        last_ghost_y = self.ghost_y
        new_x = self.x + self.velocity

        # checking if object rect is too far from bottom and top
        if self.y + self.width < 0:
            self.y = 0
        if self.y - self.width > RESOLUTION[1]:
            self.y = 0

        # does the movement step to bottom when reached right edge
        if self.x >= RESOLUTION[0]:
            new_y = self.y + self.width
            if new_y > RESOLUTION[1]:
                self.y = new_y - RESOLUTION[1]
            else:
                self.y = new_y
            self.x = self.x - RESOLUTION[0]
        else:
            self.x += self.velocity

        # check if he is on right edge
        if new_x + self.width >= RESOLUTION[0] or self.x < 0:
            self.ghost_x = True
        else:

            self.ghost_x = False

        # check if he is on top or bottom edge
        if self.y + self.height > RESOLUTION[1] or self.y < 0:
            self.ghost_y = True
        else:
            self.ghost_y = False

        # if object is on edge it makes copy of it on opposite site
        if last_ghost_y != self.ghost_y:
            if self.clone:
                # remove cloned object if no longer on edge
                self.parent.clones.remove(self)
                do_accident(self, silent=True)
            if not last_ghost_y:
               self.make_clone(self.x , self.y - RESOLUTION[1])

        # if last_ghost_x != self.ghost_x:
        #     if self.clone:
        #         # remove cloned object if no longer on edge
        #         do_accident(self, silent=True)
        #     if not last_ghost_x:
        #         self.make_clone(self.x - RESOLUTION[0], self.y + self.width )

    def make_clone(self, x, y):
        # parent object reached edge
        # it makes deepcopy of himself,
        new_car = deepcopy(self)
        self.clones.append(new_car)
        # defines who is parent and init. himself as clone
        new_car.parent = self
        new_car.clone = True
        new_car.clones = []
        # Make to clone apear on top
        new_car.x = x
        new_car.y = y
        # Adding to list of all cars
        cars.append(new_car)

    def translate_x(self):
        # gives cords on left edge translated from right edge
        return self.x - RESOLUTION[0], self.y + self.width, self.width, self.height

    def translate_y(self):
        return self.x, self.y - RESOLUTION[1], self.width, self.height

    def set_rect(self, x, y):
        self.x = x
        self.y = y

    def get_rect(self):
        return self.x, self.y, self.width, self.height

    def get_col_x(self):
        return self.x + self.width

    def get_col_y(self):
        return self.y + self.height

    def crash(self):
        self.crashed = True
        self.color = RED

    @staticmethod
    def detect_col(car1, car2):
        # method used to check if there is collision
        # i know about Rect.colliderect()
        # car1 is that behind car2
        if car1.color != car2.color:
            if abs(car1.get_col_x() - car2.get_col_x()) < car1.get_rect()[2]:
                if abs(car1.get_col_y() - car2.get_col_y()) < car1.get_rect()[3]:
                    if car2.velocity > car1.velocity:
                        car1.crashed = True
                        return car1
                    else:
                        car2.crashed = True
                        return car2
        return False


class Ghost(Car):
    # nothing
    def __init__(self, parent):
        self.parent = parent


def do_accident(car, silent=False):
    # removes car from car list
    # and adds to list of crashed cars
    global cars, cars_crashed
    print('potrącił')
    car.crash()
    if not silent:
        cars_crashed.append(car)
    try:
        cars.remove(car)
    except ValueError:
        # :^)
        pass



RESOLUTION = 1000, 500

WHITE = (0, 0, 0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
DARKBLUE = (0,0,128)
WHITE = (255,255,255)
BLACK = (0,0,0)
PINK = (255,200,200)

pygame.init()


game_display = pygame.display.set_mode(RESOLUTION)

clock = pygame.time.Clock()


cars = [] # living cars
cars_crashed = [] # crashed cars
# cars
cars.append(Car((0, 460, 30, 30), 10, PINK))
cars.append(Car((900, 244, 30, 30), 1, BLUE))
cars.append(Car((400, 42, 30, 30), 7, BLUE))
cars.append(Car((500, 490, 30, 30), 3, DARKBLUE))
cars.append(Car((500, 200, 30, 30), 2, DARKBLUE))
cars.append(Car((690, 400, 30, 30), 8, (66,66,66)))
cars.append(Car((520, 180, 30, 30), 1, GREEN))
cars.append(Car((500, 550, 30, 30), 2, (254,255,0)))
cars.append(Car((690, 400, 30, 30), 8, (66,66,66)))
cars.append(Car((520, 120, 30, 30), 1, GREEN))

# nothing
background = pygame.Surface(RESOLUTION)
dirty_rects = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            for car in cars:
                car.move()


    # check for collision
    for car1 in cars:
        for index2, car2 in enumerate(cars):
            if id(car1) == id(car2):
                # Don't check collision for himself
                continue
            if car1.parent == car2.parent:

                continue
            car = Car.detect_col(car1, car2)
            if car:

                if car.crashed and not car.crashed_check:

                    for clone in car.parent.clones:
                        print('crashing child')
                        do_accident(clone)
                    if car.parent.ghost_x:
                        # tworzy kopie samochody przesuniętą na lewą stronę mapy aby następnie
                        # umieścić ją na cmentarzysku
                        widmo = deepcopy(car)
                        widmo.parent.set_rect(car.parent.translate_x()[0], car.parent.translate_x()[1])
                        do_accident(widmo)
                    do_accident(car.parent)
                    print('crashing parent')
                    car.crashed_check = True

    # updating screens
    # dirty rects
    # no może jednak nie dirty rects
    game_display.fill(WHITE)

    # crashed cars
    for car in cars_crashed:
        pygame.draw.rect(game_display, car.color, car.get_rect())


    # working cars
    for car in cars:
        pygame.draw.rect(game_display, car.color, car.get_rect())
        if car.ghost_x:
            # this car is on the right edge of map
            # Its here to make smooth transition using just a sprite
            # The
            # TODO zaaktualizować
            pygame.draw.rect(game_display, car.color, car.translate_x())

    pygame.display.update()

    # move the cars
    for car in cars:
        car.move()

    print(len(cars))
    clock.tick(60)

