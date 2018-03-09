#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os, json
import pyglet
from lib import *
from lib.controls import *

# 定义基本变量
gamepath = os.path.dirname(os.path.realpath(__file__))

# 定义基本函数

def writefile(s, w):
	with open(s, "w", encoding = 'utf-8') as f:
		f.write(w)
def getfile(s):
	r = ''
	with open(s, "r", encoding = 'utf-8') as f:
		r = f.read()
	return r
def getobjs(s):
	# 取得 s 下所有 '.py' 文件的路径
	objs = []
	fs = os.listdir(s)
	for f in fs:
		absf = os.path.join(s, f)
		if os.path.isfile(absf) and os.path.splitext(f)[1] == '.py':
			objs.append(absf)
		elif os.path.isdir(absf):
			objs += getobjs(absf)
	return objs

# 加载配置文件
__define_files = getobjs(os.path.join(gamepath, 'define'))
__define_files.sort()
__define = {}

for i in __define_files:
	__define.update(eval(getfile(i)))

del(__define_files)

def get_define():
	r = {}
	for (key,val) in globals().items():
		if key in __define:
			r[key] = val
	return r

globals().update(__define)

# 初始化游戏库
pyglet.resource.path = RESOURCES

for i in FONTS:
	pyglet.font.add_file(os.path.join('fonts',i[0]))
	pyglet.font.load(i[1])

class GameObject(object):
	def __init__(self):
		# 定义基本变量、函数
		self.definebasicvars()
		# 创建UI
		self.build_ui()
		# 加载脚本
		self.load_scripts("__commons")
	def definebasicvars(self):
		self.exe = lambda x:exec(x,globals(),self.__dict__)
		self.val = lambda x:eval(x,globals(),self.__dict__)
	def build_ui(self):
		window = controls.Form(960,540,caption = GAME_NAME,resizable = True)
		window.set_fullscreen(FULLSCREEN)
		window.set_icon(pyglet.resource.image(ICON))
		window.set_minimum_size(960,540)
		window.set_mouse_cursor(pyglet.window.ImageMouseCursor(pyglet.resource.image(MOUSE_CURSOR), 0, 0))
		
		self.volume_music = VOLUME_MUSIC
		self.volume_effect = VOLUME_EFFECT
		self.volume_game = VOLUME_GAME
		
		root = window.root_control

		@window.event
		def on_resize(width, height):
			root.width = width
			root.height = height
			root.on_resize()
		
		pages = MultiPage((window,root))
		
		root.sons.append(pages)
		
		def hide_not_pages():
			for i in root.sons:
				if i is not pages:
					i.hide()
		
		def show():
			pages.show()
			root.visible = True
		root.show = show
		
		normal_button_back = pyglet.resource.image(NORMAL_BUTTON_BACK)
		normal_button_pressed_back = pyglet.resource.image(NORMAL_BUTTON_PRESSED_BACK)
		normal_menu_back = pyglet.resource.image(NORMAL_MENU_BACK)
		normal_slider_back = pyglet.resource.image(NORMAL_SLIDER_BACK)
		normal_slider_cursor = pyglet.resource.image(NORMAL_SLIDER_CURSOR)
		normal_checkbox_unchecked_back = pyglet.resource.image(NORMAL_CHECKBOX_UNCHECKED_BACK)
		normal_checkbox_checked_back = pyglet.resource.image(NORMAL_CHECKBOX_CHECKED_BACK)
		
		normal_title_gen = lambda parent,text,pos = ((0,0),(0,0),(1,0),(1,0)):Label((window,parent,Posattr(*pos)),pyglet.text.Label(text,font_name = NORMAL_TITLE_FONT,font_size = NORMAL_TITLE_FONT_SIZE,color = NORMAL_TITLE_COLOR, anchor_x = 'center',anchor_y = 'center'))
		
		normal_title2_gen = lambda parent,text,pos = ((0,0),(0,0),(1,0),(1,0)):Label((window,parent,Posattr(*pos)),pyglet.text.Label(text,font_name = NORMAL_TITLE2_FONT,font_size = NORMAL_TITLE2_FONT_SIZE,color = NORMAL_TITLE2_COLOR, anchor_x = 'center',anchor_y = 'center'))
		
		normal_label_gen = lambda parent,text,pos = ((0,0),(0,0),(1,0),(1,0)):Label((window,parent,Posattr(*pos)),pyglet.text.Label(text,font_name = NORMAL_LABEL_FONT,font_size = NORMAL_LABEL_FONT_SIZE,color = NORMAL_LABEL_COLOR, anchor_x = 'left',anchor_y = 'center'))
		
		normal_message_text_gen = lambda parent,text,pos = ((0,0),(0,0),(1,0),(1,0)):TextBox((window,parent,Posattr(*pos)),text,NORMAL_MESSAGE_TEXT_STYLE,multiline = True)
		
		normal_button_gen = lambda parent,labeltext,pos = ((0,0),(0,0),(1,0),(1,0)):Button(
			(window,parent,Posattr(*pos)),
			label = pyglet.text.Label(labeltext,font_name = NORMAL_BUTTON_FONT,font_size = NORMAL_BUTTON_FONT_SIZE,color = NORMAL_BUTTON_COLOR,anchor_x = 'center',anchor_y = 'center'),
			image = Sprite(normal_button_back),
			pressed_image = Sprite(normal_button_pressed_back)
		)
		
		normal_slider_gen = lambda parent,pos = ((0,0),(0,0),(1,0),(1,0)):Slider(
			(window,parent,Posattr(*pos)),
			image = Sprite(normal_slider_back),
			cursor = Sprite(normal_slider_cursor)
		)
		
		normal_checkbox_gen = lambda parent,pos = ((0,0),(0,0),(1,0),(1,0)):SwitchButton(
			(window,parent,Posattr(*pos)),
			images = (
				Sprite(normal_checkbox_unchecked_back),
				Sprite(normal_checkbox_checked_back)
			)
		)
		
		# 视频播放页
		
		media_page = MediaPlayer((window,root))
		root.sons.append(media_page)
		
		# 设置菜单
		setting_menu = MessageInteractor((window,root,Posattr(*SETTING_MENU_POS)),back = Sprite(normal_menu_back))
		
		setting_menu_title = normal_title_gen(setting_menu,SETTING_MENU_TITLE, SETTING_MENU_TITLE_POS)
		setting_menu.sons.append(setting_menu_title)
		
		setting_menu_confirm = normal_button_gen(setting_menu,SETTING_MENU_CONFIRM_TEXT,SETTING_MENU_CONFIRM_POS)
		setting_menu.sons.append(setting_menu_confirm)
		setting_menu.submit_key = (setting_menu_confirm,'on_press')
		
		setting_menu_setdefault = normal_button_gen(setting_menu,SETTING_MENU_SETDEFALUT_TEXT,SETTING_MENU_SETDEFALUT_POS)
		@setting_menu_setdefault.event
		def on_press():
			writefile(os.path.join('define','user.py'),str(get_define()))
		setting_menu.sons.append(setting_menu_setdefault)
		
		setting_menu_reset = normal_button_gen(setting_menu,SETTING_MENU_RESET_TEXT,SETTING_MENU_RESET_POS)
		@setting_menu_reset.event
		def on_press():
			writefile(os.path.join('define','user.py'),'{}')
		setting_menu.sons.append(setting_menu_reset)
		
		setting_menu_sound = Frame((window,setting_menu,Posattr(*SETTING_MENU_SOUND_FRAME_POS)))
		
		setting_menu_sound_label = normal_title2_gen(setting_menu_sound, SETTING_MENU_SOUND_TITLE, SETTING_MENU_SOUND_TITLE_POS)
		setting_menu_sound.sons.append(setting_menu_sound_label)
		
		setting_menu_volume_music = normal_slider_gen(setting_menu_sound, SETTING_MENU_VOLUME_MUSIC_POS)
		setting_menu_volume_music_label = normal_label_gen(setting_menu_sound, SETTING_MENU_VOLUME_MUSIC_TEXT, SETTING_MENU_VOLUME_MUSIC_LABEL_POS)
		@setting_menu_volume_music.event
		def on_change(val):
			self.volume_music = val
			global VOLUME_MUSIC
			VOLUME_MUSIC = val
		setting_menu_sound.sons += (setting_menu_volume_music,setting_menu_volume_music_label)
		
		setting_menu_volume_effect = normal_slider_gen(setting_menu_sound, SETTING_MENU_VOLUME_EFFECT_POS)
		setting_menu_volume_effect_label = normal_label_gen(setting_menu_sound, SETTING_MENU_VOLUME_EFFECT_TEXT, SETTING_MENU_VOLUME_EFFECT_LABEL_POS)
		@setting_menu_volume_effect.event
		def on_change(val):
			self.volume_effect = val
			global VOLUME_EFFECT
			VOLUME_EFFECT = val
		setting_menu_sound.sons += (setting_menu_volume_effect,setting_menu_volume_effect_label)
		
		setting_menu_volume_game = normal_slider_gen(setting_menu_sound, SETTING_MENU_VOLUME_GAME_POS)
		setting_menu_volume_game_label = normal_label_gen(setting_menu_sound, SETTING_MENU_VOLUME_GAME_TEXT, SETTING_MENU_VOLUME_GAME_LABEL_POS)
		@setting_menu_volume_game.event
		def on_change(val):
			self.volume_game = val
			global VOLUME_GAME
			VOLUME_GAME = val
		setting_menu_sound.sons += (setting_menu_volume_game,setting_menu_volume_game_label)
		
		setting_menu.sons.append(setting_menu_sound)
		
		setting_menu_fullscreen = normal_checkbox_gen(setting_menu,SETTING_MENU_FULLSCREEN_POS)
		setting_menu_fullscreen_label = normal_label_gen(setting_menu, SETTING_MENU_FULLSCREEN_TEXT, SETTING_MENU_FULLSCREEN_LABEL_POS)
		@setting_menu_fullscreen.event
		def on_press():
			setting_menu_fullscreen.stage ^= 1
		@setting_menu_fullscreen.event
		def on_switch(val):
			window.set_fullscreen(bool(val))
			global FULLSCREEN
			FULLSCREEN = bool(val)
		
		setting_menu.sons += (setting_menu_fullscreen, setting_menu_fullscreen_label)
		
		@setting_menu.event
		def on_show():
			setting_menu_volume_music._set_rate(self.volume_music)
			setting_menu_volume_effect._set_rate(self.volume_effect)
			setting_menu_volume_game._set_rate(self.volume_game)
			setting_menu_fullscreen._set_stage(int(window.fullscreen))
		
		root.sons.append(setting_menu)
		
		# 确认退出框
		confirm_quit = MessageBox((window,root,Posattr(*CONFIRM_QUIT_POS)),back = Sprite(normal_menu_back),layouter = MessageBox_defaultlayout_gen(TITLE_HEIGHT = 0))
		
		confirm_quit_text = normal_message_text_gen(confirm_quit,CONFIRM_QUIT_TEXT)
		confirm_quit.doc = confirm_quit_text
		
		confirm_quit_yes = normal_button_gen(confirm_quit,CONFIRM_QUIT_YES_TEXT)
		
		confirm_quit_no = normal_button_gen(confirm_quit,CONFIRM_QUIT_NO_TEXT)
		
		confirm_quit.buttons = [confirm_quit_no, confirm_quit_yes]
		
		@confirm_quit.event
		def on_submit(result):
			confirm_quit.hide()
			if result == 1:
				pyglet.app.exit()
				
		root.sons.append(confirm_quit)
		
		# 关于页面
		
		about_page = AlertBox((window,root,Posattr(*ABOUT_PAGE_POS)),
		back = Sprite(normal_menu_back),layouter = AlertBox_defaultlayout_gen(TITLE_PADDING = 50, PADDING = 30, BUTTON_X = (0.5,-95),BUTTON_WIDTH = (0,190)))
		
		about_page_title = normal_title_gen(about_page, ABOUT_PAGE_TITLE)
		about_page.title = about_page_title
		
		about_page_text = FormattedTextBox((window,about_page),pyglet.text.decode_attributed (ABOUT_PAGE_TEXT),multiline = True)
		about_page.doc = about_page_text
		
		about_page_confirm = normal_button_gen(about_page, ABOUT_PAGE_CONFIRM_TEXT)
		about_page.button = about_page_confirm
		
		about_page_watch_ed = normal_button_gen(about_page,ABOUT_PAGE_WATCH_ED_TEXT, ABOUT_PAGE_WATCH_ED_POS)
		about_page.sons.append(about_page_watch_ed)
		@about_page_watch_ed.event
		def on_press():
			hide_not_pages()
			media_page.player = pyglet.media.player.Player()
			media_page.queue(pyglet.resource.media(ED_FILE,streaming = True))
			media_page.loop = False
			@media_page.event
			def on_player_eos():
				print('debug_eos')
				media_page.hide()
				media_page.clear()
			@media_page.event
			def on_press(*args,**kw):
				print('debug_pressed')
				on_player_eos()
			media_page.play()
			media_page.show()
		
		root.sons.append(about_page)
		
		# 附录（图鉴）
		
		# appendice_page = 
		
		# 主菜单
		main_menu = ImageFrame((window,pages),back = Sprite(pyglet.resource.image(MAIN_MENU_BACK)))

		main_menu_start_button = Button(
			(window,main_menu,Posattr(*MAIN_MENU_START_POS)),
			label = pyglet.text.Label(MAIN_MENU_START_TEXT,font_name = MAIN_MENU_START_FONT,font_size = MAIN_MENU_START_FONT_SIZE,color = MAIN_MENU_START_COLOR,anchor_x = 'center',anchor_y = 'center'),
			image = Sprite(pyglet.resource.image(MAIN_MENU_START_BACK)),
			pressed_image = Sprite(pyglet.resource.image(MAIN_MENU_START_PRESSED_BACK))
		)
		main_menu.sons.append(main_menu_start_button)
		
		def main_menu_button_draw(self, event):
			def f(*args, **kw):
				if self.label is not None:
					self.label.font_name = MAIN_MENU_BUTTON_HOVERING_FONT if self.hovering else MAIN_MENU_BUTTON_FONT
				return event(*args, **kw)
			return f
		
		main_menu_button_gen = lambda pos,text:Button(
			(window,main_menu,Posattr(*pos)),
			label = pyglet.text.Label(text,font_name = MAIN_MENU_BUTTON_FONT,font_size = MAIN_MENU_BUTTON_FONT_SIZE,color = MAIN_MENU_BUTTON_COLOR, anchor_x = 'center',anchor_y = 'center')
		)
		
		main_menu_load_button =  main_menu_button_gen(MAIN_MENU_LOAD_POS,MAIN_MENU_LOAD_TEXT)
		main_menu_load_button.draw = main_menu_button_draw(main_menu_load_button, main_menu_load_button.draw)
		main_menu.sons.append(main_menu_load_button)
		
		main_menu_achievement_button = main_menu_button_gen(MAIN_MENU_ACHIEVEMENT_POS,MAIN_MENU_ACHIEVEMENT_TEXT)
		main_menu_achievement_button.draw = main_menu_button_draw(main_menu_achievement_button, main_menu_achievement_button.draw)
		main_menu.sons.append(main_menu_achievement_button)
		
		main_menu_appendice_button = main_menu_button_gen(MAIN_MENU_APPENDICE_POS,MAIN_MENU_APPENDICE_TEXT)
		main_menu_appendice_button.draw = main_menu_button_draw(main_menu_appendice_button, main_menu_appendice_button.draw)
		main_menu.sons.append(main_menu_appendice_button)
		
		main_menu_setting_button = main_menu_button_gen(MAIN_MENU_SETTING_POS,MAIN_MENU_SETTING_TEXT)
		main_menu_setting_button.draw = main_menu_button_draw(main_menu_setting_button, main_menu_setting_button.draw)
		main_menu.sons.append(main_menu_setting_button)
		
		main_menu_about_button = main_menu_button_gen(MAIN_MENU_ABOUT_POS,MAIN_MENU_ABOUT_TEXT)
		main_menu_about_button.draw = main_menu_button_draw(main_menu_about_button, main_menu_about_button.draw)
		main_menu.sons.append(main_menu_about_button)
		
		main_menu_quit_button = main_menu_button_gen(MAIN_MENU_QUIT_POS,MAIN_MENU_QUIT_TEXT)
		main_menu_quit_button.draw = main_menu_button_draw(main_menu_quit_button, main_menu_quit_button.draw)
		main_menu.sons.append(main_menu_quit_button)
		
		@main_menu_setting_button.event
		def on_press():
			hide_not_pages()
			setting_menu.show()
		
		@main_menu_about_button.event
		def on_press():
			hide_not_pages()
			about_page.show()
			
		@main_menu_quit_button.event
		def on_press():
			hide_not_pages()
			confirm_quit.show()
		
		pages.pages = [main_menu]
		
		# FPS(DEBUG)
		fps_display = pyglet.clock.ClockDisplay()
		def on_draw():
			window.clear()
			root.draw()
			fps_display.draw()
		window.on_draw = on_draw
		
		self.__dict__.update(locals())
	def set_volume_music(self,v):
		self._volume_music = v
		# update_volume
	volume_music = property(lambda self:self._volume_music,set_volume_music)
	def set_volume_effect(self,v):
		self._volume_effect = v
		# update volume
	volume_effect = property(lambda self:self._volume_effect,set_volume_effect)
	def set_volume_game(self,v):
		self._volume_game = v
		# update volume
	volume_game = property(lambda self:self._volume_game,set_volume_game)
	def load_script(self, scriptpath):
		self.exe(getfile(os.path.join(gamepath,scriptpath)))
	def load_scripts(self, scriptdir):
		objs = getobjs(os.path.join(gamepath, scriptdir))
		objs.sort()
		for i in objs:
			self.exe(getfile(i))
	def run(self):
		self.pages.page = 0
		self.window.show()
		return pyglet.app.run()

game = GameObject()
game.run()