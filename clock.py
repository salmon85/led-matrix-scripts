import time, math
from PIL import Image, ImageDraw
try:
	from rgbmatrix import RGBMatrix, RGBMatrixOptions
except:
	pass

blank_image = "black.png"


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

def clockhand(angle, length):
	"""
	Calculate the end point for the given vector.
	Angle 0 is 12 o'clock, 90 is 3 o'clock.
	Based around (32,32) as origin, (0,0) in top left.
	"""
	radian_angle = math.pi * angle / 180.0
	x = 32 + length * math.cos(radian_angle)
	y = 32 + length * math.sin(radian_angle)
	return [(32,32),(x,y)]

def clockhand2(angle, length):
	"""
	Calculate the end point for the given vector.
	Angle 0 is 12 o'clock, 90 is 3 o'clock.
	Based around (32,32) as origin, (0,0) in top left.
	"""
	radian_angle = math.pi * angle / 180.0
	x = 31 + length * math.cos(radian_angle)
	y = 31 + length * math.sin(radian_angle)
	return [(31,31),(x,y)]

def draw_face():
	background = Image.open(blank_image)
	back_img = background.copy()
	draw = ImageDraw.Draw(back_img)
	draw.ellipse((0,0,63,63), outline="#37EF50")
	draw.ellipse((1,1,62,62), outline="#37EF50")
	draw.ellipse((2,2,61,61), outline="#37EF50")
	for a in range(12):
		draw.line(clockhand2((a * 30) - 90, 30), fill ="#37EF50", width=3)
		draw.line(clockhand2((a * 30) - 90, 25), fill ="black", width=5)
	draw.rectangle([(30,30),(34,34)],fill="black")
	return back_img

def update_image(clock_face):
	back_img = clock_face.copy()
	now = time.localtime()
	draw = ImageDraw.Draw(back_img)
	draw.line(clockhand2((now.tm_min * 6) - 90, 22), fill ="blue", width=1)
	draw.line(clockhand2((now.tm_hour * 30 + now.tm_min / 2) - 90, 12), fill="yellow", width=1)
	draw.line(clockhand2(now.tm_sec * 6 - 90, 25), fill="red", width=1)
	return(back_img)

face = draw_face()
try:
	print("Press CTRL-C to stop.")
	while True:
		matrix.SetImage(update_image(face))
except KeyboardInterrupt:
	sys.exit(0)
