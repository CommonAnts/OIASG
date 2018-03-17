# importing system modules

import os
import traceback

from lib import *

# import game lib
# import pygame
# from pygame.locals import *
# importing my modules

try:
	ini.init_sys()


	# debugging mode:read operations from console

	def start_game(scenario):
		g = game.gameplay(scenario, os.path.dirname(os.path.realpath(__file__)))
		g.run()


	while True:
		ope = input()
		print("Main system got operation:" + ope)
		exec(ope)
except:
	print("!!!!! --- 主程序抛出异常 --- !!!!!")
	traceback.print_exc()

exit()
