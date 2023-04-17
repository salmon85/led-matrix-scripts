# led-matrix-scripts
scripts for my 64x64 led matrix being ran by a pi zero




snake.py
requires rgbmatrix, pygame

a test of a clone of the nokia snake game written in pygame. used a ps3 controller connected via bluetooth / usb to the pi

run: python3 snake.py



image-viewer-animated.py
requires rgbmatrix

originally started as a script that would display a 64x64 image onto the matrix, but became more when I split animated images up into their individual frames and displayed them in a loop.

run: python3 image-viewer-animated.py imagefile brightness%
note: anything over 50% brightness is very bright, will increase power usage as well as give out more heat on the led's.



clock.py
requires rgbmatrix

takes the system time and displays it on an analog clock (completely drawn with the PIL module)

run: python3 clock.py

stream.py
requires rgbmatrix, streamlink

takes a twitch stream, pulls the 160p stream from it and attempts to display it on the matrix

run: python3 stream.py
note: the streamurl needs to be changed in the script to the one of your choosing
the stream in 160p is still too large for the matrix
sometimes the stream doesn't load and you will get a purple screen... because twitch
the pi zero isn't powerful enough to do this in realtime. There will be a delay and noticable frame speed differences.
