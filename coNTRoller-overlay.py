#! /d/python3/python

import argparse
import struct
import time
import pygame
import distutils.util
from PyNTR.PyNTR import PyNTR

class InputState:

	def __init__(self, client):
		self.client = client

	def update(self):
		base = 0x10000000

		combined_state = self.client.ReadU64(base + 0x1C)
		[
			pad_state,
			unused_pad_state,
			self.circle_x,
			self.circle_y,
		] = (struct.unpack('hhhh', combined_state.to_bytes(8, 'little')))

		[
			self.button_a,
			self.button_b,
			self.button_select,
			self.button_start,
			self.button_right,
			self.button_left,
			self.button_up,
			self.button_down,
			self.button_r,
			self.button_l,
			self.button_x,
			self.button_y,
			_,_,_,_,
		] = map(distutils.util.strtobool, list(format(pad_state, '016b'))[::-1])

	def print(self):
		print('=======================')
		print('button_a',     self.button_a)
		print('button_b',     self.button_b)
		print('button_select',self.button_select)
		print('button_start', self.button_start)
		print('button_right', self.button_right)
		print('button_left',  self.button_left)
		print('button_up',    self.button_up)
		print('button_down',  self.button_down)
		print('button_r',     self.button_r)
		print('button_l',     self.button_l)
		print('button_x',     self.button_x)
		print('button_y',     self.button_y)
		print('circle_x',     self.circle_x)
		print('circle_y',     self.circle_y)
		print('=======================')

def color(s):
	try:
		(r,g,b) = map(int, s.split(','))
		return r,g,b
	except:
		raise argparse.ArgumentTypeError('Color must be r,g,b')

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Input display for NTR connected 3DS')
	parser.add_argument('ip', metavar='IP', help='Local IP of your 3DS')
	parser.add_argument('-bg', '--background-color', metavar='COLOR', type=color, default='255,255,255', help='background color as 3 values, e.g. 255,255,255')
	args = parser.parse_args()
	print(args)

	pygame.init()

	client = PyNTR(args.ip)
	client.start_connection()
	client.send_hello_packet()
	pid = client.set_game_name('hid')

	input_state = InputState(client)

	overlay_img      = pygame.image.load('ds_overlay.png')
	circle_stick_img = pygame.image.load('circle_stick.png')

	display_width = overlay_img.get_width()
	display_height = overlay_img.get_height()
	pygame.display.set_caption('NTR-controller-display')

	game_display = pygame.display.set_mode((display_width, display_height))
	button_surface = pygame.Surface((display_width, display_height), pygame.SRCALPHA)

	clock = pygame.time.Clock()

	closed = False

	def overlay():
		game_display.blit(overlay_img, (0, 0))

	def circle_stick(centre, circle_x, circle_y):
		movement_factor = 200
		midpoint = 2048
		x = centre[0] - (circle_stick_img.get_width()/2)  + (circle_x - midpoint)/movement_factor
		y = centre[1] - (circle_stick_img.get_height()/2) - (circle_y - midpoint)/movement_factor
		game_display.blit(circle_stick_img, (x, y))

	def button_circle(centre, radius, state):
		if state:
			pygame.draw.circle(button_surface, (0, 0, 0, 128), centre, radius)
	
	def button_rect(rect, state):
		if state:
			pygame.draw.rect(button_surface, (0, 0, 0, 128), rect)
	
	while not closed:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				closed = True

		input_state.update()
		#input_state.print()

		game_display.fill(args.background_color)
		button_surface.fill((0,0,0,0))
		overlay()
		circle_stick((48, 51), input_state.circle_x, input_state.circle_y)
		button_circle((440,  76), 12, input_state.button_a)
		button_circle((415,  99), 12, input_state.button_b)
		button_circle((415,  52), 12, input_state.button_x)
		button_circle((390,  76), 12, input_state.button_y)

		button_circle((390, 152), 7,  input_state.button_start)
		button_circle((390, 181), 7,  input_state.button_select)

		button_rect(( 20, 116, 18, 18), input_state.button_left)
		button_rect(( 56, 116, 18, 18), input_state.button_right)
		button_rect(( 39,  98, 18, 18), input_state.button_up)
		button_rect(( 39, 135, 18, 18), input_state.button_down)

		button_rect((  0,   0, 40, 17), input_state.button_l)
		button_rect((424,   0, 40, 17), input_state.button_r)

		game_display.blit(button_surface, (0,0))
		pygame.display.update()
		clock.tick(60)

	pygame.quit()
	quit()
