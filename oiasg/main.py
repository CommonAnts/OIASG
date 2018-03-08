#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os, json
import pyglet
from lib import *
from lib.controls import *

# 定义基本变量
gamepath = os.path.dirname(os.path.realpath(__file__))

# 定义基本函数

def getobj(s):
	return open(s, "r", encoding = 'utf-8').read()
def getobjs(s):
	# 取得 s 下所有 '.py' 文件的路径
	objs = []
	fs = os.listdir(s)
	for f in fs:
		absf = os.path.join(s, f)
		if os.path.isfile(absf) and os.path.splitext(f)[1] == '.py':
			objs.append(absf)
		elif os.path.isdir(absf):
			objs += getobjs(absf)
	return objs

# 加载配置文件
define = json.loads(getobj('define.json'))


# 初始化游戏库
pyglet.resource.path = define['resources']

pyglet.font.add_file(os.path.join('fonts','杨任东竹石体-Regular.ttf'))
pyglet.font.load('杨任东竹石体-Regular')
pyglet.font.add_file(os.path.join('fonts','杨任东竹石体-Semibold.ttf'))
pyglet.font.load('杨任东竹石体-Semibold')

class GameObject(object):
	def __init__(self):
		# 定义基本变量、函数
		self.definebasicvars()
		# 创建UI
		self.build_ui()
		# 加载脚本
		self.load_scripts("__commons")
	def definebasicvars(self):
		self.exe = lambda x:exec(x,globals(),self.__dict__)
		self.val = lambda x:eval(x,globals(),self.__dict__)
	def build_ui(self):
		window = controls.Form(960,540,caption = define['GAME_NAME'],resizable = True)
		self.window = window
		window.set_minimum_size(960,540)
		root = window.root_control
		self.root = root

		@self.window.event
		def on_resize(width, height):
			root.width = width
			root.height = height
			root.on_resize()
		
		pages = MultiPage((window,root))
		self.pages = pages
		
		root.sons.append(pages)
		
		main_menu = ImageFrame((window,pages),back = Sprite(pyglet.resource.image('main_back.png')))
		self.main_menu = main_menu

		main_menu_start_button = Button(
			(window,main_menu,Posattr((1,-526),(0.5,-48),(0,526),(0,96))),
			label = pyglet.text.Label(define['MAIN_MENU_START_TEXT'],font_name = define['MAIN_MENU_START_FONT'],font_size=44,anchor_x = 'center',anchor_y = 'center'),
			image = Sprite(pyglet.resource.image('tag_button_v.png')),
			pressed_image = Sprite(pyglet.resource.image('tag_button_v_pressed.png'))
		)
		self.main_menu_start_button = main_menu_start_button
		main_menu.sons.append(main_menu_start_button)
		
		# main_menu_load_button = Button(
			# (window,main_menu,Posattr((1,-526),(0.5,-48),(0,526),(0,96)))
		# )
		
		pages.pages = [self.main_menu]
		
		# FPS(DEBUG)
		fps_display = pyglet.clock.ClockDisplay()
		def on_draw():
			window.clear()
			root.draw()
			fps_display.draw()
		self.window.on_draw = on_draw
	def load_script(self, scriptpath):
		self.exe(getobj(os.path.join(gamepath,scriptpath)))
	def load_scripts(self, scriptdir):
		objs = getobjs(os.path.join(gamepath, scriptdir))
		objs.sort()
		for i in objs:
			self.exe(getobj(i))
	def run(self):
		self.pages.page = 0
		# self.window.set_fullscreen(True)
		self.window.show()
		return pyglet.app.run()

game = GameObject()
game.run()