
import pygame
from scipy.io import wavfile
import pyaudio
import wave
import os
import time
import numpy as np
import serial
import struct
from math import *
import matplotlib.pyplot as plt

CHUNK = 2**11
# screen = pygame.display.set_mode((840,620))
# while 1:
#
#     event = pygame.event.wait()
#
#     if event.type == pygame.QUIT:
#             pygame.quit()
#             quit()
#
#
# ser = serial.Serial("COM3", 9600)
# ser.flushInput()
# ser.flushOutput()
# time.sleep(3)
sound = wave.open("cypis.wav")

p = pyaudio.PyAudio()
print(p.get_device_count())
[print(p.get_device_info_by_index(x)) for x in range(p.get_device_count())]


#foobar_stram = p.open(format)
foobar_stream = p.open(format = pyaudio.paInt16,
                              channels =2,
                              rate = 44100 * 1,
                              input = True,
                              input_device_index = 0
                              )
stream = p.open(format = pyaudio.paInt16,
                channels=1,
                rate=44100*2,
                output=True,
                )

data = sound.readframes(CHUNK)



while len(data) > 0:
    stream.write(data)
    data_bar = foobar_stream.read(CHUNK)
    data = sound.readframes(CHUNK)
    data = data_bar

    #data = stream.read(CHUNK, exception_on_overflow = False)


    new_data = np.fromstring(data, dtype=np.int16)


    masked = np.ma.masked_less(new_data,0)
    try:
        av = int(masked.mean())
    except np.ma.core.MaskError:
        pass
    if av > 17000:
        av = 17000
    vol = av//170
    color = int(((av/17)%255))
    os.system("cls")
    print('vol',vol )
    print('Color',color )
    #ser.write(struct.pack('>BB', vol % 255,  vol % 255))




#
#
#

