#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

import pyglet
from .lib import *
from .lib.data import data, saves
from .lib.resource import resource
from .lib.ui import ui

GAMEPATH = os.path.dirname(os.path.realpath(__file__))


class GameObject(object):
	# 游戏体（单类）
	def __init__(self):
		# 加载数据
		data.init(GAMEPATH)
		# 加载存档
		saves.init(GAMEPATH)
		# 加载资源
		resource.init()
		# 创建UI
		ui.init()

	def run(self):
		# 显示UI
		ui.show()
		# 运行应用程序
		pyglet.app.run()
		# 保存数据
		data.save()


game = GameObject()
game.run()
