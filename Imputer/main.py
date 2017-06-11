from test import ClipBoard
import keyboard
from imagemanager import ImageManager

import os
print(__file__)
print(os.path)
path = os.path.dirname(__file__)
image_path = os.path.join(path,'images')
images = ImageManager('images/')


def call(tag):
    p = images.get_from_tag(tag)
    ClipBoard.paste(os.path.join(image_path, p))

def make(name):
    print('making:', name)
    return lambda: call(name)

for tag in images.tags:
    keyboard.add_word_listener('.'+tag, make(tag), timeout=0)

keyboard.wait()