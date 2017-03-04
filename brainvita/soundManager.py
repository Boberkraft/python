import pygame
from enum import Enum


class Level(Enum):
    Normal, Hard, Hardcore = range(3)


class SoundManager:
    def __init__(self, lvl):
        self.lvl = lvl

    def play_background(self):
        pygame.mixer.music.load('music/%d_background.mp3' % self.lvl)
        pygame.mixer.music.play()

    def play_sound(self):
        effect = pygame.mixer.Sound('sound/%d_move.mp3' % self.lvl)
        effect.play()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_mode((100, 100))

    while True:
        x = pygame.Rect(0,0,50,50)
        print(x.center)
        pass
