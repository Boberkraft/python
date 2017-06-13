from PIL import Image

import win32clipboard
from io import BytesIO
from time import sleep
import win32com.client
import keyboard
import pythoncom
import os

import sys

class ClipBoard:
    @classmethod
    def send_to_clipboard(cls, clip_type, data):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(clip_type, data)
        win32clipboard.CloseClipboard()

    @classmethod
    def erase(cls, name):
        for _ in name+' ':
            keyboard.send('backspace')

    @classmethod
    def paste(cls, file, tag):
        path = os.path.join('uploads/', file)
        image = Image.open(path)

        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()

        cls.send_to_clipboard(win32clipboard.CF_DIB, data)
        pythoncom.CoInitialize()
        shell = win32com.client.Dispatch("WScript.Shell")
        cls.erase(tag)
        shell.SendKeys('^(v)')

if __name__ == '__main__':

    # keyboard.hook_key('a', keydown_callback=xd)
    keyboard.add_word_listener('69sad', sad    , timeout=0)
    keyboard.add_word_listener('69angry', angry, timeout=0)
    keyboard.add_word_listener('69happy', happy, timeout=0)
    keyboard.add_word_listener('69prorok', prorok, timeout=0)
    keyboard.wait()
