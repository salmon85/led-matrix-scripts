import os
os.environ["PYGAME_FREETYPE"] = "1"
import pygame, time, random, sys, math
from PIL import Image
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame.freetype
pygame.init()
pygame.freetype.init()

# how many joysticks connected to computer?
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
	# if no joysticks, quit program safely
	print ("Error, I did not find any joysticks")
else:
	# initialise joystick
	print("Found Joystick")
	joystick = pygame.joystick.Joystick(0)
	joystick.init()

from rgbmatrix import RGBMatrix, RGBMatrixOptions
options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.brightness=35
options.chain_length = 1
options.gpio_slowdown = 4
options.parallel = 1
options.hardware_mapping = 'regular-pi1'  # If you have an Adafruit HAT: 'adafruit-hat'
matrix = RGBMatrix(options = options)


white = (255,255,255)
black = (0,0,0)
orange = (255,165,0)
width, height = 64, 64
game_display = pygame.Surface((width,height))

clock = pygame.time.Clock()
snake_size = 4
snake_speed = 2

message_font = pygame.freetype.Font(r"./fonts/4x6.bdf")

def hex_to_RGB(hex):
	# Pass 16 to the integer function for change of base
	return [int(hex[i:i+2], 16) for i in range(1,6,2)]

def RGB_to_hex(RGB):
	# Components need to be integers for hex to make sense
	RGB = [int(x) for x in RGB]
	return "#"+"".join(["0{0:x}".format(v) if v < 16 else
						"{0:x}".format(v) for v in RGB])

def color_dict(gradient):
	return {"hex":[RGB_to_hex(RGB) for RGB in gradient],
			"r":[RGB[0] for RGB in gradient],
			"g":[RGB[1] for RGB in gradient],
			"b":[RGB[2] for RGB in gradient]}

def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
	# Starting and ending colors in RGB form
	s = hex_to_RGB(start_hex)
	f = hex_to_RGB(finish_hex)
	# Initilize a list of the output colors with the starting color
	RGB_list = [s]
	# Calcuate a color at each evenly spaced value of t from 1 to n
	for t in range(1, n):
		# Interpolate RGB vector for color at the current value of t
		curr_vector = [
			int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
			for j in range(3)
		]
		# Add it to our list of output colors
		RGB_list.append(curr_vector)
	
	return color_dict(RGB_list)

def polylinear_gradient(colors, n):
	''' returns a list of colors forming linear gradients between
		all sequential pairs of colors. "n" specifies the total
		number of desired output colors '''
	# The number of colors per individual linear gradient
	n_out = int(float(n) / (len(colors) - 1))
	# returns dictionary defined by color_dict()
	gradient_dict = linear_gradient(colors[0], colors[1], n_out)
	
	if len(colors) > 1:
		for col in range(1, len(colors) - 1):
			next = linear_gradient(colors[col], colors[col+1], n_out)
			for k in ("hex", "r", "g", "b"):
				# Exclude first point to avoid duplicates
				gradient_dict[k] += next[k][1:]
	
	return gradient_dict

c1 = RGB_to_hex((255,43,43))
c2 = RGB_to_hex((255,250,43))
c3 = RGB_to_hex((43,255,69))
c4 = RGB_to_hex((43,69,255))
c5 = RGB_to_hex((255,43,250))
gradient = polylinear_gradient((c1,c2,c3,c4,c5),int(int((width/snake_size))*int((height/snake_size))))
def draw_snake(snake_size, snake_pixels):
	for pixel in reversed(snake_pixels):
		try:
			colour = (int(gradient["r"][len(snake_pixels)-snake_pixels.index(pixel)-1]), int(gradient["g"][len(snake_pixels)-snake_pixels.index(pixel)-1]),int(gradient["b"][len(snake_pixels)-snake_pixels.index(pixel)-1]))
			pygame.draw.rect(game_display, colour, [pixel[0], pixel[1], snake_size, snake_size])
		except:
			pygame.draw.rect(game_display, white, [pixel[0], pixel[1], snake_size, snake_size])


def menu():
	game_close = False
	while not game_close:
		game_display.fill(black)
		#menu1, unused = message_font.render("SNAKE!", (99, 155, 255))
		#menu2, unused = message_font.render("X or Space", (255, 255, 255))
		#menu3, unused = message_font.render("To Start", (255, 255, 255))
		#game_display.blit(menu1, (10, 20))
		#game_display.blit(menu2, (10, 30))
		#game_display.blit(menu3, (10, 40))
		snake_splash = pygame.image.load("snake.bmp")
		game_display.blit(snake_splash, (0, 0))
		pil_string_image = pygame.image.tostring(game_display, "RGBA", False)
		pil_image = Image.frombytes("RGBA", (64, 64),pil_string_image)
		matrix.SetImage(pil_image.convert("RGB"))
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					game_close = True
			if event.type == pygame.JOYBUTTONDOWN:
				if event.button == 0:
					game_close = True
	
def run_game():
	game_over = False
	game_close = False
	x, y = (width/2), (height/2)
	x_speed = 0
	y_speed = 0
	snake_pixels = []
	snake_length = 1
	target_x = round(random.randrange(0, width -snake_size) / snake_size) * snake_size
	target_y = round(random.randrange(0, height -snake_size) / snake_size) * snake_size
	score = 0
	
	last_press = ""
	last_move = ""
	while not game_close:
		while not game_over:
			game_display.fill(black)
			pygame.draw.rect(game_display, orange, [target_x, target_y, snake_size, snake_size])
			if x > width -snake_size or x < 0 or y > height-snake_size or y < 0:
				game_over = True
			x += x_speed
			y += y_speed
			snake_pixels.append([x,y])
			if len(snake_pixels) > snake_length:
				del snake_pixels[0]
			for pixel in snake_pixels[:-1]:
				if pixel == [x, y]:
					game_over = True
				if pixel == [target_x, target_y]:
					target_x = round(random.randrange(0, width -snake_size) / snake_size) * snake_size
					target_y = round(random.randrange(0, height -snake_size) / snake_size) * snake_size
			draw_snake(snake_size, snake_pixels)
			
			if x == target_x and y == target_y:
				target_x = round(random.randrange(0, width -snake_size) / snake_size) * snake_size
				target_y = round(random.randrange(0, height -snake_size) / snake_size) * snake_size
				snake_length += 1
				score +=1
			clock.tick(int(snake_speed + round(1*(score / 2))))
			pil_string_image = pygame.image.tostring(game_display, "RGBA", False)
			pil_image = Image.frombytes("RGBA", (64, 64),pil_string_image)
			matrix.SetImage(pil_image.convert("RGB"))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					game_over = True
				if len(snake_pixels) > 1:
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_LEFT and x -snake_size != snake_pixels[-2][0]:
							last_press = "Left"
							x_speed = -snake_size
							y_speed = 0
						if event.key == pygame.K_RIGHT and x +snake_size != snake_pixels[-2][0]:
							last_press = "Right"
							x_speed = snake_size
							y_speed = 0
						if event.key == pygame.K_UP and y -snake_size != snake_pixels[-2][1]:
							last_press = "Up"
							x_speed = 0
							y_speed = -snake_size
						if event.key == pygame.K_DOWN and y +snake_size != snake_pixels[-2][1]:
							last_press = "Down"
							x_speed = 0
							y_speed = snake_size
					if event.type == pygame.JOYHATMOTION:
						if event.value[0] == -1 and x -snake_size != snake_pixels[-2][0]:
							last_press = "Left"
							x_speed = -snake_size
							y_speed = 0
						if event.value[0] == 1 and x +snake_size != snake_pixels[-2][0]:
							last_press = "Right"
							x_speed = snake_size
							y_speed = 0
						if event.value[1] == 1 and y -snake_size != snake_pixels[-2][1]:
							last_press = "Up"
							x_speed = 0
							y_speed = -snake_size
						if event.value[1] == -1 and y +snake_size != snake_pixels[-2][1]:
							last_press = "Down"
							x_speed = 0
							y_speed = snake_size
					if event.type == pygame.JOYBUTTONDOWN:
						if event.button == 13 and y -snake_size != snake_pixels[-2][1]:
							last_press = "Up"
							x_speed = 0
							y_speed = -snake_size
						if event.button == 14 and y +snake_size != snake_pixels[-2][1]:
							last_press = "Down"
							x_speed = 0
							y_speed = snake_size
						if event.button == 15 and x -snake_size != snake_pixels[-2][0]:
							last_press = "Left"
							x_speed = -snake_size
							y_speed = 0
						if event.button == 16 and x +snake_size != snake_pixels[-2][0]:
							last_press = "Right"
							x_speed = snake_size
							y_speed = 0
				else:
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_LEFT and last_move != "Right":
							last_press = "Left"
							x_speed = -snake_size
							y_speed = 0
						if event.key == pygame.K_RIGHT and last_move != "Left":
							last_press = "Right"
							x_speed = snake_size
							y_speed = 0
						if event.key == pygame.K_UP and last_move != "Down":
							last_press = "Up"
							x_speed = 0
							y_speed = -snake_size
						if event.key == pygame.K_DOWN and last_move != "Up":
							last_press = "Down"
							x_speed = 0
							y_speed = snake_size
					if event.type == pygame.JOYHATMOTION:
						if event.value[0] == -1 and last_move != "Right":
							last_press = "Left"
							x_speed = -snake_size
							y_speed = 0
						if event.value[0] == 1 and last_move != "Left":
							last_press = "Right"
							x_speed = snake_size
							y_speed = 0
						if event.value[1] == 1 and last_move != "Down":
							last_press = "Up"
							x_speed = 0
							y_speed = -snake_size
						if event.value[1] == -1 and last_move != "Up":
							last_press = "Down"
							x_speed = 0
							y_speed = snake_size
					if event.type == pygame.JOYBUTTONDOWN:
						if event.button == 13 and last_move != "Down":
							last_press = "Up"
							x_speed = 0
							y_speed = -snake_size
						if event.button == 14 and last_move != "Up":
							last_press = "Down"
							x_speed = 0
							y_speed = snake_size
						if event.button == 15 and last_move != "Right":
							last_press = "Left"
							x_speed = -snake_size
							y_speed = 0
						if event.button == 16 and last_move != "Left":
							last_press = "Right"
							x_speed = snake_size
							y_speed = 0
			last_move = last_press
		else:
			game_display.fill(black)
			game_over_message, unused = message_font.render("Game Over!", (255, 0, 0))
			score_message, unused = message_font.render("Score: "+str(score), (255, 255, 255))
			scorefile = open("snake_scores.txt", 'r').read()
			try:
				top_score = int(scorefile)
			except:
				top_score = 0
				scorefile = open("snake_scores.txt", 'w+')
				scorefile.write(str(top_score))
				scorefile.close()
			scorefile = open("snake_scores.txt", 'r').read()
			top_score = int(scorefile)
			if score > top_score:
				top_score = score
				scorefile = open("snake_scores.txt", 'w+')
				scorefile.write(str(top_score))
				scorefile.close()
			top_score_message, unused = message_font.render("Best: "+str(top_score), (255, 255, 255))
			game_display.blit(game_over_message, (10, 20))
			game_display.blit(score_message, (10, 30))
			game_display.blit(top_score_message, (10, 40))
			pil_string_image = pygame.image.tostring(game_display, "RGBA", False)
			pil_image = Image.frombytes("RGBA", (64, 64),pil_string_image)
			matrix.SetImage(pil_image.convert("RGB"))
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						game_over = False
						game_close = True
				if event.type == pygame.JOYBUTTONDOWN:
					if event.button == 0:
						game_over = False
						game_close = True
while True:
	menu()
	run_game()
