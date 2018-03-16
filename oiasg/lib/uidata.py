#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pyglet
from .controls import *
from .data import *
from .resource import *
from .gameobjects import *
from . import ui

class UIData_Base(object):
	def build_control(self):
		pass
	@property
	def control(self):
		# 生成控件
		if not self._built_control:
			self._control = self.build_control()
			self._built_control = True
		return self._control
# UI数据：从某个字典项读取数据并生成UI数据（仅外观）
class UIData_DictItem(UIData_Base):
	def __init__(self, data):
		key, value = data
		self.__dict__.update(value)
		self.key = key
		self._built_control = False
class UIData(UIData_Base):
	def __init__(self, data):
		self.data = data
		self._built_control = False
# 静态UI数据集：静态（类）存储的UI数据
class UIDataStaticSet(object):
	@classmethod
	def build_dataset(cls):
		pass
	@classmethod
	def dataset(cls):
		# 生成控件
		if not cls._built_dataset:
			cls._dataset = cls.build_dataset()
			cls._built_dataset = True
		return cls._dataset
		
class Contest_UIData(UIData):
	def build_control(self):
		image = None if self.data.image is None else Sprite(resource.load_image(self.data.image))
		title = self.data.name
		info = []
		for key,value in self.data.data.items():
			info.append((value.strftime(ui.GAME_CHARACTER_BOARD_BIRTH_FORMAT)) if key == 'birth' else str(value))
		return image,title,info
class Message_Log_UIData(UIData):
	def build_control(self):
		button_text = self.data.time.strftime(self.data.timeformat) + ' ' + self.data.name
		button_label = pyglet.text.Label(button_text,font_name = self.data.font_name if self.data.font_name is not None else ui.GAME_MESSAGE_FONT_NAME,font_size = ui.GAME_MESSAGE_FONT_SIZE,color = self.data.font_color,anchor_x = 'center',anchor_y = 'center')
		button = Button([ui.ui.window], label = button_label,
			image = Sprite(ui.ui.game_message_log_back),
			hover_color = ui.NORMAL_BUTTON_HOVER_COLOR,
			color = ui.NORMAL_BUTTON_COLOR)
		messagewindow = ui.ui.MessageWindow(self.data.text, self.data.name, Sprite(resource.load_image(self.data.image)) if self.data.image is not None else None, self.data.pos)
		@button.event
		def on_press():
			messagewindow.exe()
		return button
class Message_Timetable_UIData(UIData):
	def build_control(self):
		button_text = self.data.time.strftime(self.data.timeformat) + ' ' + self.data.name
		button_label = pyglet.text.Label(button_text,font_name = self.data.font_name if self.data.font_name is not None else ui.GAME_MESSAGE_FONT_NAME,font_size = ui.GAME_MESSAGE_FONT_SIZE,color = self.data.font_color,anchor_x = 'center',anchor_y = 'center')
		button = Button([ui.ui.window], label = button_label,
			image = Sprite(ui.ui.game_message_timetable_back),
			hover_color = ui.NORMAL_BUTTON_HOVER_COLOR,
			color = ui.NORMAL_BUTTON_COLOR)
		messagewindow = ui.ui.MessageWindow(self.data.text, self.data.name, Sprite(resource.load_image(self.data.image)) if self.data.image is not None else None, self.data.pos)
		@button.event
		def on_press():
			messagewindow.exe()
		return button
class Strategy_UIData(UIData):
	def build_control(self):
		button_label = pyglet.text.Label(self.data.name,font_name = ui.GAME_STRATEGY_FONT_NAME,font_size = ui.GAME_STRATEGY_FONT_SIZE,color = ui.GAME_STRATEGY_FONT_COLOR,anchor_x = 'center',anchor_y = 'center')
		icon = Sprite(resource.load_image(self.data.icon)) if self.data.icon is not None else None
		button = SwitchButton(
			[ui.ui.window],
			[button_label,button_label],
			[Sprite(ui.ui.game_message_strategy_back),Sprite(ui.ui.game_message_strategy_select_back)],
			[icon,icon],
			hover_color = ui.NORMAL_BUTTON_HOVER_COLOR,
			color = ui.NORMAL_BUTTON_COLOR
		)
		return button
class Image_UIData(UIData):
	def build_control(self):
		return Sprite(resource.load_image(self.data))
class GameUIDataManager(object):
	def __init__(self, game):
		self.game = game
		self.images_uidata = {}
		self.character_uidata = None
		self.messages_log_uidata = {}
		self.messages_timetable_uidata = {}
		self.messages_strategies_uidata = {}
		self.strategies_uidata = {}
	
	def get_image(self, key):
		if key not in self.images_uidata:
			self.images_uidata[key] = Image_UIData(key)
		res = self.images_uidata[key].control
		res.key = key
		return res
	def get_message_log_button(self, key):
		if key not in self.messages_log_uidata:
			self.messages_log_uidata[key] = Message_Log_UIData(self.game.gamedata['messages'][key])
		res = self.messages_log_uidata[key].control
		res.key = key
		return res
	def get_message_timetable_button(self, key):
		if key not in self.messages_timetable_uidata:
			self.messages_timetable_uidata[key] = Message_Timetable_UIData(self.game.gamedata['messages'][key])
		res = self.messages_timetable_uidata[key].control
		res.key = key
		return res
	def get_message_strategy_button(self, key):
		if key not in self.messages_strategies_uidata:
			self.messages_strategies_uidata[key] = Strategy_UIData(self.game.gamedata['strategies'][key])
		res = self.messages_strategies_uidata[key].control
		res.key = key
		return res
	def get_strategy_button(self, key):
		if key not in self.strategies_uidata:
			self.strategies_uidata[key] = Strategy_UIData(self.game.gamedata['strategies'][key])
		res = self.strategies_uidata[key].control
		res.key = key
		return res
		
	@property
	def character_board_ui(self):
		if self.character_uidata is None:
			self.character_uidata = Contest_UIData(self.game.gamedata['character'])
		return self.character_uidata.control
	def flush_character_board_ui(self):
		self.character_uidata = None
		
	@property
	def messages_board_ui(self):
		plans = self.game.gamedata['strategy_plans']
		
		strategy_board_items = []
		if plans:
			it = self.game.gamedata['strategy_plan_it'] % len(plans)
			for i in range(min(len(plans),ui.GAME_MESSAGES_BOARD_PLAN_ITEM_COUNT)):
				strategy_board_items.append(self.get_message_strategy_button(plans[it]))
				it = (it + 1)%len(plans)
			
		return list(map(self.get_message_timetable_button, self.game.gamedata['timetable_messages'][-ui.GAME_MESSAGES_BOARD_TIMETABLE_ITEM_COUNT:])),list(map(self.get_message_log_button, self.game.gamedata['log_messages'][-ui.GAME_MESSAGES_BOARD_LOG_ITEM_COUNT:])), strategy_board_items, list(map(self.get_strategy_button, self.game.gamedata['select_strategies']))
	
	@property
	def pages_character_ui(self):
		back, front = None, None
		if self.game.gamedata['pages_character_back'] is not None:
			back = self.get_image(self.game.gamedata['pages_character_back'])
		if self.game.gamedata['pages_character_front'] is not None:
			front = self.get_image(self.game.gamedata['pages_character_front'])
		return back, front
		
	@property
	def time(self):
		return self.game.gamedata['time']
		