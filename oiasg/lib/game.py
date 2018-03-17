#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
import pyglet

from .resource import resource
from .gameobjects import *
from .uidata import *
from . import ui

def build_from_data(cls, data):
	res = cls()
	res.__dict__.update(data)
	return res
	
# 一局游戏的抽象模型
# UI 与此模型分离，此模型通过调用UI的接口交互
class GamePlay(pyglet.event.EventDispatcher):
	# gamedata:游戏数据
	def __init__(self, gamedata = None, load_from_save = False):
		game = self
		self.game = self
		self.data = data
		self.resource = resource
		self.ui = ui.ui
		self._load_from_save = load_from_save
		self.gamedata = gamedata if gamedata is not None else {}
		self.ui_data = GameUIDataManager(self)
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
		self.StrategyPlan = StrategyPlan
	def _init_system_data(self):
		self.speed = 0
	def _init_game_data(self):
		self.exe(self.data.get(['GAME_INIT_SCRIPT'],''))
	def _load_define(self):
		# 初始化基本数据
		self.gamedata.update(self.data.get_all_dict(['GENERAL_GAME_DEFINE']))
		# 初始化角色（注意这个不是从全局加载）
		self.gamedata['character'] = build_from_data(Character, self.gamedata.get('CHARACTER',{}))
		# 初始化事件
		events = self.data.get_all_dict(['EVENTS'])
		self.gamedata['events'].update({key:build_from_data(Event, val) for key, val in events.items()})
		# 初始化策略
		strategies = self.data.get_all_dict(['STRATEGIES'])
		self.gamedata['strategies'].update({key:build_from_data(Strategy, val) for key, val in strategies.items()})
	def _init_data(self):
		if not self._load_from_save:
			# 加载游戏全局常量数据（如事件、比赛、TAG等）
			self._load_define()
			# 初始化基本数据
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
	def pause(self):
		self.speed = 0
	def _set_current_strategy(self, value):
		self.gamedata['current_strategy'] = value
		self.dispatch_event('on_update_message')
	current_strategy = property(lambda self:self.gamedata['current_strategy'],_set_current_strategy)
	def play_round(self, dt):
		self.exe(self.data.get(['PLAY_ROUND_SCRIPT'],''))
		self.dispatch_event('on_update')
	def _play(self):
		self._init_data()
		self.dispatch_event('on_update')
	def _end(self):
		pyglet.clock.unschedule(self.play_round)
		self.__dict__.clear()
GamePlay.register_event_type('on_update')
GamePlay.register_event_type('on_update_speed_time')
GamePlay.register_event_type('on_update_message')
GamePlay.register_event_type('on_update_pages_character')
