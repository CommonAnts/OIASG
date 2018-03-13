import os
import time
import traceback
# import functools

from . import appearance

def getobj(s):
	return open(s, "r", encoding = 'utf-8').read()

def getobjs(s):
	objs = []
	fs = os.listdir(s)
	for f in fs:
		absf = os.path.join(s, f)
		if os.path.isfile(absf) and os.path.splitext(f)[1] == '.py':
			objs.append(absf)
		elif os.path.isdir(absf):
			objs += getobjs(absf)
	return objs
		
class gameplay(object):
	def __init__(self, scenario = "__general", _basedir = None):
		print("A new game object is constructed.")
		if _basedir is None:
			_basedir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
		self.__basedir = _basedir
		self.var = {
			"load_script":self.load_script,
			"load_scripts":self.load_scripts,
			
			"running":True
			# "output":self.output
		}
		self.load_scripts("__commons")
		
		self.load_script(os.path.join("scenarios",scenario + '.py'))
		
		self.paused = True
		self.speed = 0
		
	def end(self):
		print("A game has ended.")
	def run(self):
		print("A game has started.")
		try:
			# definition
			# execution
			while self.var['running']:
				self.var['play_round']()
				self.pause_game()
				while self.paused:
					# self.output()
					ope = input()
					# print("Game object got operation:" + ope)
					exec(ope)
				time.sleep(2*(0.5**self.speed))
		except:
			print("!!!!! --- 游戏体抛出异常 --- !!!!!")
			traceback.print_exc()
		self.end()
	def output(self):
		print(self.var)
	def load_script(self, scriptpath):
		exec(getobj(os.path.join(self.__basedir,scriptpath)), self.var, self.var)
	def load_scripts(self, scriptdir):
		objs = getobjs(os.path.join(self.__basedir, scriptdir))
		objs.sort()
		for i in objs:
			exec(getobj(i), self.var, self.var)
	def pause_game(self):
		self.paused = True
	def continue_game(self):
		self.paused = False
	def set_speed(self, speed):
		self.speed = speed