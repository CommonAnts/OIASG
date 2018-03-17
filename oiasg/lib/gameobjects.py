#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime

_DEFAULT_TIME = datetime.datetime(2018,1,1)
_DEFAULT_TIMEDELTA = datetime.timedelta(0)
class Event(object):
	def __init__(self, trigger = 'False', effect = '', privilege = 0):
		self.__dict__.update({key:value for key,value in locals().items() if key != 'self'})
	def check(self, game):
		return bool(game.val(self.trigger))
	def exe(self, game):
		game.exe(self.effect)

class Character(object):
	def __init__(self, name = '', image = None, data = None):
		if data is None:
			data = {}
		self.__dict__.update({key:value for key,value in locals().items() if key != 'self'})
		
class Strategy(object):
	def __init__(self, event = None, name = '', icon = None):
		self.__dict__.update({key:value for key,value in locals().items() if key != 'self'})
class StrategyPlan(object):
	def __init__(self, plan = None, name = ''):
		if plan is None:
			plan = []
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
	def __init__(self, name = '', time = _DEFAULT_TIME, timeformat = '', text = '', image = None, font_name = None, font_color = (0,0,0,255), pos = None):
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
