#!/usr/bin/python
# -*- coding: UTF-8 -*-

# UI数据：从define的某个字典项读取数据并生成UI数据（仅外观）
class UIData(object):
	def __init__(self, data):
		key, value = data
		self.__dict__.update(value)
		self.key = key
		self._built_control = False
	def build_control(self):
		pass
	@property
	def control(self):
		# 生成控件
		if not self._built_control:
			self._control = self.build_control()
			self._built_control = True
		return self._control
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
		