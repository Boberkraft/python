import keyboard
import requests
from PIL import Image
from io import BytesIO
from clipboard import ClipBoard
import requests
import shutil



class Client:

    def listen(self):
        while True:
            keyboard.wait('.')
            typed = keyboard.record(' ')
            tag = ''.join(keyboard.get_typed_strings(typed))
            self.paste_image(tag)

    def paste_image(self, tag):
        print('pripering')
        r = requests.get('http://localhost:5000/get_image/{}'.format(tag))

        if r.status_code == 200 and r.text:
            path = r.text
            ClipBoard.paste(path, tag)



cl = Client()
cl.listen()