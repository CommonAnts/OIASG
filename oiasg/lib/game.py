#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
import pyglet
from .ui import *
from .uidata import *

_DEFAULT_TIME = datetime.datetime(2018,1,1)
_DEFAULT_TIMEDELTA = datetime.timedelta(0)
class Event(object):
	def __init__(self, trigger = 'False', effect = '', privilege = 0):
		self.__dict__.update({key:value for key,value in locals().items() if key != 'self'})
	def check(self, game):
		return bool(game.val(self.trigger))
	def exe(self, game):
		game.exe(self.effect)

class Strategy(object):
	def __init__(self, event = None, name = '', icon = None):
		self.__dict__.update({key:value for key,value in locals().items() if key != 'self'})

class Ability(object):
	name = ''
	val = 0
class BasicAbility(Ability):
	def __init__(self, page = None, name = '', color = (0,0,0)):
		self.__dict__.update({key:value for key,value in locals().items() if key != 'self'})
class KnowledgeAbility(Ability):
	visible = False
	privilege = 0
	def __init__(self, page = None, name = '', text = '', icon = None, image = None, parent = None, difficulty = 0):
		self.__dict__.update({key:value for key,value in locals().items() if key != 'self'})

class AbilityPage(object):
	def __init__(self, name = '', icon = None, image = None):
		self.__dict__.update({key:value for key,value in locals().items() if key != 'self'})

class MessageItem(object):
	def __init__(self, name = '', time = _DEFAULT_TIME, timeformat = '', text = '', image = None, font_name = None, font_color = (0,0,0)):
		self.__dict__.update({key:value for key,value in locals().items() if key != 'self'})

class SolVertice(object):
	visible = False
	rate = 0
	error = 0
	def __init__(self, ability = None, parent = None):
		self.__dict__.update({key:value for key,value in locals().items() if key != 'self'})
class SolGraph(object):
	def __init__(self, vertices = None):
		if vertices is None:
			vertices = []
		self.__dict__.update({key:value for key,value in locals().items() if key != 'self'})
class Problem(object):
	idea = None
	code = None
	def __init__(self, idea = None, code = None):
		self.vertices = {}

class Contest(object):
	def __init__(self, name = '', image = None, problems = None, start_time = _DEFAULT_TIME, end_time = _DEFAULT_TIME, time_delta = _DEFAULT_TIMEDELTA, ranklist = None):
		if problems is None:
			problems = {}
		if ranklist is None:
			ranklist = lambda:{}
		self.__dict__.update({key:value for key,value in locals().items() if key != 'self'})
# 一局游戏的抽象模型
# UI 与此模型分离，此模型通过调用UI的接口交互
class GamePlay(pyglet.event.EventDispatcher):
	# gamedata:游戏数据
	def __init__(self, data, ui, gamedata = None, load_from_save = False):
		game = self
		self.game = self
		self.data = data
		self.ui = ui
		self._load_from_save = load_from_save
		self.gamedata = gamedata if gamedata is not None else {}
		self.exe = lambda x:exec(x,self.__dict__,self.gamedata)
		self.val = lambda x:eval(x,self.__dict__,self.gamedata)
		# 初始化游戏数据
		self.dispatch_game_event = self.dispatch_event
		
		self.Event = Event
		self.Strategy = Strategy
		self.Ability = Ability
		self.BasicAbility = BasicAbility
		self.KnowledgeAbility = KnowledgeAbility
		self.AbilityPage = AbilityPage
		self.MessageItem = MessageItem
		self.SolVertice = SolVertice
		self.SolGraph = SolGraph
		self.Problem = Problem
		self.Contest = Contest
	def _init_system_data(self):
		self.speed = 0
	def _init_game_data(self):
		self.exe(self.data.get(['GAME_INIT_SCRIPT'],''))
	def _load_define(self):
		self.gamedata.update(self.data.get_all_dict(['GENERAL_GAME_DEFINE']))
		def build_from_data(cls, data):
			res = cls()
			res.__dict__.update(data)
			return res
		events = self.data.get_all_dict(['EVENTS'])
		self.gamedata['events'].update({key:build_from_data(self.Event, val) for key, val in events.items()})
	def _init_data(self):
		# 加载游戏全局常量数据（如事件、比赛、TAG等）
		self._load_define()
		# 初始化基本数据
		if not self._load_from_save:
			self._init_game_data()
		# 初始化游戏系统
		self._init_system_data()
	def _set_speed(self,speed):
		self._speed = speed
		# 设置游戏速度
		pyglet.clock.unschedule(self.play_round)
		if speed > 0:
			pyglet.clock.schedule_interval(self.play_round, self.data.get(['GAME_TIME_INTERVAL'])[speed])
		self.dispatch_event('on_update_speed_time')
	speed = property(lambda self:self._speed,_set_speed)
	def play_round(self, dt):
		self.exe(self.data.get(['PLAY_ROUND_SCRIPT'],''))
		self.dispatch_event('on_update')
	def _play(self):
		self._init_data()
	@property
	def time(self):
		return self.gamedata['time']
	def pause(self):
		self.speed = 0
GamePlay.register_event_type('on_update')
GamePlay.register_event_type('on_update_speed_time')
