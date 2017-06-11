from flask import Flask
from DataManager import DataManager
import os
app = Flask(__name__)


def get_names():
    image_list = 'images.txt'
    return DataManager.get('images/{}'.format(image_list))

def get_images():
    pass

@app.route('/')
def root():
    data = get_names()
    print(data)
    return 'testior'

app.run()


