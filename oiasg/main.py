#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import pyglet
from lib import *
from lib.ui import *
from lib.data import *
from lib.controls import *
from lib.resource import *

GAMEPATH = os.path.dirname(os.path.realpath(__file__))
class GameObject(object):
	# 游戏体（单类）
	def __init__(self):
		# 加载数据
		self.data = Data(GAMEPATH)
		# 加载存档
		self.saves = GameSaveManager(GAMEPATH)
		# 加载资源
		self.resource = Resource(self.data)
		# 创建UI
		self.ui = UI(self)
	def run(self):
		# 显示UI
		self.ui.show()
		# 运行应用程序
		pyglet.app.run()
		# 保存数据
		self.data.save()

game = GameObject()
game.run()