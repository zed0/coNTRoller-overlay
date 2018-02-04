#! /d/python3/python

import struct
import time
from PyNTR import PyNTR

class InputState:

	def __init__(self, client):
		self.client = client

	def update(self):
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
		] = list(format(pad_state, '016b'))[::-1]

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

if __name__ == '__main__':
	print("Starting the programm..")
	client = PyNTR('192.168.1.164')

	print("Starting the connection..")
	client.start_connection()

	print("Sending a 'hello' packet..")
	client.send_hello_packet()

	pid = client.set_game_name('hid')
	print(pid)

	base = 0x10000000
	data = client.ReadU64(base)
	print("svcGetSystemTick count: %x" % data)

	input_state = InputState(client)
	while(True):
		input_state.update()
		input_state.print()
		time.sleep(0.5)
