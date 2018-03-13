#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

import pyglet

class Resource(object):
	def __init__(self,data):
		self.data = data
		pyglet.resource.path = data.get_subdirs('resources')
		self.load_fonts(data.get_all_list(['FONTS']))
	def load_fonts(self,fonts):
		if fonts is not None:
			for font in fonts:
				pyglet.resource.add_font(font[0])
				pyglet.font.load(font[1])
	def load_image(self,path):
		if os.path.splitext(path)[1].lower() == '.gif':
			return pyglet.resource.animation(path)
		else:
			return pyglet.resource.image(path)
	def load_static_image(self,path):
		return pyglet.resource.image(path)
	def decode_text(self,str):
		if len(str) < 1:
			return pyglet.text.decode_text(str)
		elif str[0] == 'N':
			# 游戏默认格式
			return self.default_formatted_text(str[1:])
		elif str[0] == 'H':
			# HTML
			return pyglet.text.decode_html(str[1:])
		elif str[0] == 'P':
			# 纯文本
			return pyglet.text.decode_text(str[1:])
		else:
			# pyglet标准格式
			return pyglet.text.decode_attributed(str[1:])
	def default_formatted_text(self,str):
		return self.decode_text('F'+self.data.get(['UI','NORMAL_MESSAGE_TEXT_STYLE_TEXT'],'')+str)
