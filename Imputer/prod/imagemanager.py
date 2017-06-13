from DataManager import DataManager
from random import randint

class ImageManager:

    def __init__(self, path):
        self.path = path
        self.conf = 'images.txt'
        self.load()

    def load(self):
        self.tags = DataManager.get(self.path + self.conf)

    def get_from_tag(self, tag, num=None):
        in_tag = self.tags[tag]
        if num is None:
            num = randint(0, len(in_tag) - 1)

        if isinstance(in_tag, list):
            return in_tag[num]
        else:
            # there is single image in that tag
            return in_tag

    def add(self, tag, name):
        pass

if __name__ == '__main__':
    images = ImageManager('images/')
    print(images.tags)
    print(images.get_from_tag('sad'))