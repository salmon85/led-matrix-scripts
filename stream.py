import subprocess as sp
import streamlink, time
from PIL import Image

try:
	from rgbmatrix import RGBMatrix, RGBMatrixOptions
except:
	pass

try:
	# Configuration for the matrix
	options = RGBMatrixOptions()
	options.rows = 64
	options.cols = 64
	options.brightness=35
	options.chain_length = 1
	options.parallel = 1
	options.gpio_slowdown = 4
	options.hardware_mapping = 'regular-pi1'  # If you have an Adafruit HAT: 'adafruit-hat'
	matrix = RGBMatrix(options = options)
except:
	pass


url = "https://twitch.tv/bisnap"
stream_url = streamlink.streams(url)["160p"].url # 284x160

command = [ "ffmpeg",
			'-i', stream_url,
			'-loglevel', 'quiet',
			'-an',
			'-f', 'image2pipe',
			'-pix_fmt', 'rgb24',
			'-vcodec', 'rawvideo', '-']

pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)

print(stream_url)
while True:
	raw_image = pipe.stdout.read(284*160*3)
	new_image = Image.frombytes("RGB", (284,160), raw_image)
	pipe.stdout.flush()
	im1 = new_image.resize((64, 36))
	matrix.SetImage(im1)
	#new_image.show()
	#time.sleep(5)