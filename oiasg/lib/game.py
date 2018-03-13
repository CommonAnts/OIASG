#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
import pyglet
from .ui import *

class Contest(pyglet.event.EventDispatcher):
	def __init__(self, game, data):
		self.game = game
		self.data = data
# 一局游戏的抽象模型
# UI 与此模型分离，此模型通过调用UI的接口交互
class GamePlay(pyglet.event.EventDispatcher):
	# gamedata:游戏数据
	def __init__(self, data, ui, gamepage, gamedata = None, load_from_save = False):
		self.data = data
		self.ui = ui
		self.gamepage = gamepage
		self.load_from_save = load_from_save
		self.gamedata = gamedata if gamedata is not None else {}
		self.exe = lambda x:exec(x,self.__dict__,self.gamedata)
		self.val = lambda x:eval(x,self.__dict__,self.gamedata)
		# 初始化游戏数据
	def init_system_data(self):
		self.game_speed = 0
		self.contest = None
	def init_game_data(self):
		self.exe(self.data.get(['GAME_INIT_SCRIPT'],''))
	def load_define(self):
		pass
	def init_data(self):
		# 加载游戏全局常量数据（如事件、比赛、TAG等）
		self.load_define()
		# 初始化基本数据
		if not self.load_from_save:
			self.init_game_data()
		# 初始化游戏系统
		self.init_system_data()
	def _set_game_speed(self,speed):
		self._game_speed = speed
		# 设置游戏速度
		self.gamepage.set_speed(speed)
		pyglet.clock.unschedule(self.play_round)
		if speed > 0:
			pyglet.clock.schedule_interval(self.play_round, self.data.get(['GAME_TIME_INTERVAL'])[speed])
	game_speed = property(lambda self:self._game_speed,_set_game_speed)
	def play_round(self, dt):
		self.exe(self.data.get(['PLAY_ROUND_SCRIPT'],''))
	def play(self):
		self.init_data()
	@property
	def time(self):
		return self.gamedata['time']
	def pause(self):
		self.game_speed = 0