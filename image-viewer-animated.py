#!/usr/bin/env python
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
from PIL import GifImagePlugin

if len(sys.argv) < 3:
    sys.exit("Usage: image-viewer-animated.py <image> <brightness %>")
else:
    image_file = sys.argv[1]
    brightness = sys.argv[2]

image = Image.open(image_file)

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.brightness=int(brightness)
options.chain_length = 1
options.gpio_slowdown=4
options.parallel = 1
options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)


try:
    if image.is_animated:
        while True:
            for frame in range(0,image.n_frames):
                image.seek(frame)
                matrix.SetImage(image.convert('RGB'))
    else:
        matrix.SetImage(image.convert('RGB'))
except:
    matrix.SetImage(image.convert('RGB'))

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)
