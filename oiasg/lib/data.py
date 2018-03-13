#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 全局数据文件模块

import os, hashlib, pickle, datetime

def _md5_checksum(obj):
	md5_gen = hashlib.md5()
	md5_gen.update(pickle.dumps(obj))
	return md5_gen.hexdigest()

class DataFileIO(object):
	# 数据交互接口
	@staticmethod
	def set_file(s, w):
		# 写文件
		with open(s, "w", encoding = 'utf-8') as f:
			f.write(str(w))
	@staticmethod
	def get_file(s):
		# 读文件
		r = ''
		with open(s, "r", encoding = 'utf-8') as f:
			r = f.read()
		return eval(r)

class FileSystemIO(object):
	@staticmethod
	def _get_py_paths(path):
		objs = []
		files = os.listdir(path)
		for file in files:
			abs_path = os.path.join(path, file)
			if os.path.isfile(abs_path) and os.path.splitext(file)[1].lower() == '.py':
				objs.append(abs_path)
			elif os.path.isdir(abs_path):
				objs += FileSystemIO._get_py_paths(abs_path)
		return objs
	@staticmethod
	def get_py_paths(path):
		# 取得 path 下所有 '.py' 文件的绝对路径
		objs = FileSystemIO._get_py_paths(path)
		objs.sort()
		return objs
	@staticmethod
	def get_subdirs(path):
		# 取得 path 所有子目录的绝对路径
		objs = []
		files = os.listdir(path)
		for file in files:
			abs_path = os.path.join(path, file)
			if os.path.isdir(abs_path):
				objs.append(abs_path)
		return objs
# 抽象数据系统
class DataSet(object):
	# 读写数据文件
	def __init__(self, path, readonly = False):
		self.readonly = readonly
		self.PATH = path
		self.load()
	def save(self):
		# [(file,data)]
		if self.readonly:
			return False
		for file in self.data:
			DataFileIO.set_file(file[0],file[1])
		return True
	def load(self):
		files = FileSystemIO.get_py_paths(self.PATH)
		self.data = []
		for file in files:
			self.data.append((file,DataFileIO.get_file(file)))
	def get(self,key_seq,default = None):
		for i in self.data:
			d = i[1]
			got = True
			for j in key_seq:
				if j in d:
					d = d[j]
				else:
					got = False
					break
			if got:
				return d
		return default
	def set(self,key_seq, value):
		if self.readonly:
			return False
		for i in self.data:
			d = i[1]
			got = True
			for j in key_seq:
				if j in d:
					d = d[j]
				else:
					got = False
					break
			if got:
				d = i[1]
				for j in key_seq[:-1]:
					d = d[j]
				d[key_seq[-1]] = value
				return True
		return False
	def checksum(self):	
		return _md5_checksum(self.data)

class GameVersion(object):
	def __init__(self, data = None):
		if data is None:
			self.checksum = ''
			self.name = ''
		else:
			dlc_versions = [i.version for i in data.dlcs]
			
			dlc_md5s = [i.checksum for i in dlc_versions]
			dlc_md5s.append(data._self_md5_checksum())
			self.checksum = _md5_checksum(dlc_md5s)
			
			dlc_names = [i.name for i in dlc_versions]
			dlc_names.append(data._package_name())
			self.name = dlc_names
	def __eq__(self, x):
		if isinstance(x, GameVersion):
			return self.checksum == x.checksum
		else:
			return False
	def _name_to_str(self, name, depth):
		__SEPARATE = '    '
		if isinstance(name, list):
			res = __SEPARATE*depth + name[1] + '\n'
			for i in name[0]:
				res += self._name_to_str(i, depth+1)
			return res
		else:
			return __SEPARATE*depth + name + '\n'
	def name_to_str(self):
		return self._name_to_str(self.name, 0)+'\n'
	def checksum_to_str(self):
		return self.checksum[:16]
# 数据管理器
class Data(object):
	def __init__(self, game_path):
		self._checksum = None
		self.PATH = game_path
		self.define = DataSet(os.path.join(self.PATH,'define'), readonly = True)
		self.data = DataSet(os.path.join(self.PATH,'data'), readonly = False)
		self.dlcs = self._get_dlcs()
		self._version = None
	def _self_md5_checksum(self):
		return _md5_checksum(self.define)
	def _package_name(self):
		return self.define.get(['PACKAGE_NAME'],'')
	@property
	def version(self):
		if self._version is not None:
			return self._version
		self._version = GameVersion(self)
		return self._version
	def save(self):
		self.data.save()
		for i in self.dlcs:
			i.save()
	def _get_dlcs(self):
		dlcs = []
		dlcpath = os.path.join(self.PATH,'dlcs')
		if os.path.isdir(dlcpath):
			dlc_paths = FileSystemIO.get_subdirs(dlcpath)
			dlcs = [Data(dlc_path) for dlc_path in dlc_paths]
		return dlcs
	def get(self, key_seq, default = None):
		res = None
		for i in range(len(self.dlcs)-1,-1,-1):
			if res is None:
				res = self.dlcs[i].get(key_seq)
		if res is None:
			res = self.data.get(key_seq)
		if res is None:
			res = self.define.get(key_seq)
		if res is None:
			res = default
		return res
	def get_all(self, key_seq):
		res = []
		for i in range(len(self.dlcs)-1,-1,-1):
			t = self.dlcs[i].get(key_seq)
			if t is not None:
				res += t
		t = self.data.get(key_seq)
		if t is not None:
			res.append(t)
		t = self.define.get(key_seq)
		if t is not None:
			res.append(t)
		return res
	def get_all_list(self, key_seq):
		t = self.get_all(key_seq)
		res = []
		for i in t:
			res += i
		return res
	def get_all_dict(self, key_seq):
		t = self.get_all(key_seq)
		res = {}
		for i in t:
			res.update(i)
		return res
	def set(self, key_seq, value):
		res = False
		for i in range(len(self.dlcs)-1,-1,-1):
			if not res:
				res = self.dlcs[i].set(key_seq, value)
		if not res:
			res = self.data.set(key_seq, value)
		return res
	def get_subdirs(self, path):
		# 取得所有DLC的path子目录（如果存在）
		res = []
		self_path = os.path.join(self.PATH, path)
		if os.path.isdir(self_path):
			res.append(self_path)
		for i in self.dlcs:
			res += i.get_subdirs(path)
		return res

class SaveFileIO(object):
	@staticmethod
	def set_file(file, data):
		with open(file, 'wb') as f:
			pickle.dump(data, f)
	@staticmethod
	def get_file(file):
		with open(file, 'rb') as f:	
			return pickle.load(f)
		return None
	@staticmethod
	def remove_file(file):
		try:
			os.remove(file)
		finally:
			pass

_SAVE_EXT = '.oiasgsav'
# 存档管理器
class GameSaveManager(object):
	def __init__(self, game_path):
		self.PATH = game_path
		self.savepath = os.path.join(game_path, 'saves')
		if not os.path.isdir(self.savepath):
			os.makedirs(self.savepath)
	def get_save_abspath(self, savename):
		return os.path.join(self.savepath,savename + _SAVE_EXT)
	def get_save_names(self):
		# 得到所有存档的名称
		objs = []
		files = os.listdir(self.savepath)
		for file in files:
			ext = os.path.splitext(file)
			if ext[1].lower() == _SAVE_EXT:
				objs.append(ext[0])
		return objs
	def trans_name(self,name):
		# 过滤存档名的关键字符
		return name.translate(str.maketrans("""|\?*<":>+[]/'""",' '*13))
	def test_save_exists(self,save):
		# 指定名称的存档是否存在
		return os.path.isfile(self.get_save_abspath(save))
	def get_available_save_name(self):
		# 获得一个合法的未使用的存档名
		i = 0
		gname = lambda i:('save%s' % i)
		while self.test_save_exists(gname(i)):
			i += 1
		return gname(i)
	def save(self, name, gamedata):
		SaveFileIO.set_file(self.get_save_abspath(name), gamedata)
	def load(self, name):
		return SaveFileIO.get_file(self.get_save_abspath(name))
	def remove(self, name):
		SaveFileIO.remove_file(self.get_save_abspath(name))