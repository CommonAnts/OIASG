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
def load_datafile(s):
	globals().update(eval(getfile(os.path.join(gamepath,os.path.join('data',s)))))
def save_datafile(s, data):
	writefile(os.path.join(gamepath,os.path.join('data',s)),str(data))
def getobjs(s):
	# 取得 s 下所有 '.py' 文件的路径
	objs = []
	fs = os.listdir(s)
	for f in fs:
		absf = os.path.join(s, f)
		if os.path.isfile(absf) and os.path.splitext(f)[1].lower() == '.py':
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

def get_settings():
	r = {}
	for (key,val) in globals().items():
		if key in SETTING_KEYS:
			r[key] = val
	return r

globals().update(__define)

# 初始化游戏库
pyglet.resource.path = RESOURCES

for i in FONTS:
	pyglet.resource.add_font(i[0])
	pyglet.font.load(i[1])

def load_image(path):
	if os.path.splitext(path)[1].lower() == '.gif':
		return pyglet.resource.animation(path)
	else:
		return pyglet.resource.image(path)
def decode_text(str):
	if len(str) < 1:
		return pyglet.text.decode_text(str)
	elif str[0] == 'H':
		return pyglet.text.decode_html(str[1:])
	elif str[0] == 'P':
		return pyglet.text.decode_text(str[1:])
	else:
		return pyglet.text.decode_attributed(str[1:])
class GameObject(object):
	def __init__(self):
		# 定义基本变量、函数
		self.definebasicvars()
		# 加载基本数据文件
		self.load_datafiles("data")
		# 加载脚本
		self.load_scripts("commons")
		# 配置基本设置
		self.init_settings()
		# 创建UI
		self.build_ui()
	def __del__(self):
		# 保存全局数据
		self.save_datafiles()
	def definebasicvars(self):
	# 定义基本变量、函数
		self.exe = lambda x:exec(x,globals(),self.__dict__)
		self.val = lambda x:eval(x,globals(),self.__dict__)
	def load_datafiles(self, datadir):
	# 加载全局数据
		objs = getobjs(os.path.join(gamepath, datadir))
		objs.sort()
		for i in objs:
			globals().update(self.val(getfile(i)))
	def save_datafiles(self):
	# 存储全局数据
		pass
	def load_script(self, scriptpath):
	# 加载单个脚本
		self.exe(getfile(os.path.join(gamepath,scriptpath)))
	def load_scripts(self, scriptdir):
	# 加载脚本
		objs = getobjs(os.path.join(gamepath, scriptdir))
		objs.sort()
		for i in objs:
			self.exe(getfile(i))
	def init_settings(self):
		self.volume_music = VOLUME_MUSIC
		self.volume_effect = VOLUME_EFFECT
		self.volume_game = VOLUME_GAME
	def build_ui(self):
	# 创建UI并注册事件
		window = controls.Form(960,540,caption = GAME_NAME,resizable = True)
		window.set_fullscreen(FULLSCREEN)
		window.set_icon(pyglet.resource.image(ICON))
		window.set_minimum_size(960,540)
		window.set_mouse_cursor(pyglet.window.ImageMouseCursor(pyglet.resource.image(MOUSE_CURSOR), 0, 0))
		
		# 控件生成器
		
		normal_button_back = load_image(NORMAL_BUTTON_BACK)
		normal_button_pressed_back = load_image(NORMAL_BUTTON_PRESSED_BACK)
		normal_menu_back = load_image(NORMAL_MENU_BACK)
		normal_page_back = load_image(NORMAL_PAGE_BACK)
		normal_default_image = load_image(NORMAL_DEFAULT_IMAGE)
		normal_slider_back = load_image(NORMAL_SLIDER_BACK)
		normal_slider_cursor = load_image(NORMAL_SLIDER_CURSOR)
		normal_checkbox_unchecked_back = load_image(NORMAL_CHECKBOX_UNCHECKED_BACK)
		normal_checkbox_checked_back = load_image(NORMAL_CHECKBOX_CHECKED_BACK)
		normal_scrollbar_back = load_image(NORMAL_SCROLLBAR_BACK)
		normal_scrollbar_cursor = load_image(NORMAL_SCROLLBAR_CURSOR)
		normal_switchbutton_back = load_image(NORMAL_SWITCHBUTTON_BACK)
		normal_switchbutton_select_back = load_image(NORMAL_SWITCHBUTTON_SELECT_BACK)
		normal_tag_rv_back = load_image(NORMAL_TAG_RV_IMAGE)
		normal_tag_rv_selected_back = load_image(NORMAL_TAG_RV_SELECTED_IMAGE)
		
		normal_title0_gen = lambda parent,text,pos = DEFAULT_POS:Label((window,parent,Posattr(*pos)),pyglet.text.Label(text,font_name = NORMAL_TITLE0_FONT,font_size = NORMAL_TITLE0_FONT_SIZE,color = NORMAL_TITLE0_COLOR, anchor_x = 'center',anchor_y = 'center'))
		normal_title_gen = lambda parent,text,pos = DEFAULT_POS:Label((window,parent,Posattr(*pos)),pyglet.text.Label(text,font_name = NORMAL_TITLE_FONT,font_size = NORMAL_TITLE_FONT_SIZE,color = NORMAL_TITLE_COLOR, anchor_x = 'center',anchor_y = 'center'))
		normal_title2_gen = lambda parent,text,pos = DEFAULT_POS:Label((window,parent,Posattr(*pos)),pyglet.text.Label(text,font_name = NORMAL_TITLE2_FONT,font_size = NORMAL_TITLE2_FONT_SIZE,color = NORMAL_TITLE2_COLOR, anchor_x = 'center',anchor_y = 'center'))
		normal_label_gen = lambda parent,text,pos = DEFAULT_POS:Label((window,parent,Posattr(*pos)),pyglet.text.Label(text,font_name = NORMAL_LABEL_FONT,font_size = NORMAL_LABEL_FONT_SIZE,color = NORMAL_LABEL_COLOR, anchor_x = 'left',anchor_y = 'center'))
		normal_message_text_gen = lambda parent,text,pos = DEFAULT_POS:TextBox((window,parent,Posattr(*pos)),text,NORMAL_MESSAGE_TEXT_STYLE,multiline = True)
		normal_buttonlabel_gen = lambda text:pyglet.text.Label(text,font_name = NORMAL_BUTTON_FONT,font_size = NORMAL_BUTTON_FONT_SIZE,color = NORMAL_BUTTON_FONT_COLOR,anchor_x = 'center',anchor_y = 'center')
		normal_button_gen = lambda parent,labeltext,pos = DEFAULT_POS:Button(
			(window,parent,Posattr(*pos)),
			label = normal_buttonlabel_gen(labeltext),
			image = Sprite(normal_button_back),
			pressed_image = Sprite(normal_button_pressed_back),
			hover_color = NORMAL_BUTTON_HOVER_COLOR,
			color = NORMAL_BUTTON_COLOR
		)
		normal_slider_gen = lambda parent,pos = DEFAULT_POS:Slider(
			(window,parent,Posattr(*pos)),
			image = Sprite(normal_slider_back),
			cursor = Sprite(normal_slider_cursor)
		)
		normal_checkbox_gen = lambda parent,pos = DEFAULT_POS:SwitchButton(
			(window,parent,Posattr(*pos)),
			images = (
				Sprite(normal_checkbox_unchecked_back),
				Sprite(normal_checkbox_checked_back)
			),
			hover_color = NORMAL_BUTTON_HOVER_COLOR,
			color = NORMAL_BUTTON_COLOR
		)
		normal_formatted_text_gen = lambda parent,text,pos = DEFAULT_POS:FormattedTextBox((window,parent,Posattr(*pos)),decode_text(text),multiline = True)
		normal_scrollbar_gen = lambda parent,pos = DEFAULT_POS:ScrollBar((window,parent,Posattr(*pos)), image = Sprite(normal_scrollbar_back), cursor = Sprite(normal_scrollbar_cursor))
		def normal_switchbutton_gen(parent,text,pos = DEFAULT_POS):
			title = normal_buttonlabel_gen(text)
			r = SwitchButton(
				(window,parent,pos),
				[title,title],
				[Sprite(normal_switchbutton_back),Sprite(normal_switchbutton_select_back)],
				hover_color = NORMAL_BUTTON_HOVER_COLOR,
				color = NORMAL_BUTTON_COLOR
			)
			return r
		def normal_tag_rv_gen(parent,text,pos = DEFAULT_POS):
			title = normal_buttonlabel_gen(text)
			r = SwitchButton(
				(window,parent,pos),
				[title,title],
				[Sprite(normal_tag_rv_back),Sprite(normal_tag_rv_selected_back)],
				hover_color = NORMAL_BUTTON_HOVER_COLOR,
				color = NORMAL_BUTTON_COLOR
			)
			return r
		def normal_scrolltext_gen(parent,text,pos = DEFAULT_POS):
			r = ScrollTextBox((window,parent,Posattr(*pos)))
			doc = normal_message_text_gen(r,text)
			scrollbar = normal_scrollbar_gen(r)
			r.doc = doc
			r.scrollbar = scrollbar
			return r
		def normal_scrollformattedtext_gen(parent,text,pos = DEFAULT_POS):
			r = ScrollTextBox((window,parent,Posattr(*pos)))
			doc = normal_formatted_text_gen(r,text)
			scrollbar = normal_scrollbar_gen(r)
			r.doc = doc
			r.scrollbar = scrollbar
			return r
			
		root = window.root_control
		
		def remove_sons(control):
			while root.sons and root.sons[-1] is not control:
				root.sons.pop()
		def remove_control(control):
			while root.sons:
				flag = root.sons[-1] is control
				root.sons.pop()
				if flag:
					break
		def push_control(control):
			root.sons.append(control)
			root.on_resize()
			control.show()
		def alert(text, title, pos = NORMAL_ALERT_POS):
			alert_box = AlertBox((window,root,Posattr(*pos)),back = Sprite(normal_menu_back),layouter = AlertBox_defaultlayout_gen())
			alert_text = normal_message_text_gen(alert_box,text)
			alert_box.doc = alert_text
			alert_title = normal_title_gen(alert_box,title)
			alert_box.title = alert_title
			alert_button = normal_button_gen(alert_box,NORMAL_ALERT_BUTTON_TEXT)
			alert_box.button = alert_button
			@alert_box.event
			def on_submit():
				remove_control(alert_box)
			push_control(alert_box)
			return alert_box
		def alert_notitle(text, pos = NORMAL_ALERT_NOTITLE_POS):
			alert_box = AlertBox((window,root,Posattr(*pos)),back = Sprite(normal_menu_back),layouter = AlertBox_defaultlayout_gen(TITLE_HEIGHT = 0))
			alert_text = normal_message_text_gen(alert_box,text)
			alert_box.doc = alert_text
			alert_button = normal_button_gen(alert_box,NORMAL_ALERT_BUTTON_TEXT)
			alert_box.button = alert_button
			@alert_box.event
			def on_submit():
				remove_control(alert_box)
			push_control(alert_box)
			return alert_box
		def play_media_page(media, loop = False):
			media_page = MediaPlayer((window,root))
			media_page.player = pyglet.media.player.Player()
			media_page.queue(media)
			media_page.loop = loop
			media_page.play()
			@media_page.event
			def on_player_eos():
				media_page.clear()
				remove_control(media_page)
			@media_page.event
			def on_press(*args,**kw):
				on_player_eos()
			push_control(media_page)
		
		# 设置菜单
		def show_setting_menu():
			def build_setting_menu():
				setting_menu = MessageInteractor((window,root,Posattr(*SETTING_MENU_POS)),back = Sprite(normal_menu_back))
				
				title = normal_title_gen(setting_menu,SETTING_MENU_TITLE, SETTING_MENU_TITLE_POS)
				setting_menu.sons.append(title)
				
				confirm = normal_button_gen(setting_menu,SETTING_MENU_CONFIRM_TEXT,SETTING_MENU_CONFIRM_POS)
				setting_menu.sons.append(confirm)
				setting_menu.submit_key = (confirm,'on_press')
				
				setdefault = normal_button_gen(setting_menu,SETTING_MENU_SETDEFALUT_TEXT,SETTING_MENU_SETDEFALUT_POS)
				@setdefault.event
				def on_press():
					self.save_settings()
				setting_menu.sons.append(setdefault)
				
				reset = normal_button_gen(setting_menu,SETTING_MENU_RESET_TEXT,SETTING_MENU_RESET_POS)
				@reset.event
				def on_press():
					self.reset_settings()
					alert_notitle('下次启动时生效')
				setting_menu.sons.append(reset)
				
				sound = Frame((window,setting_menu,Posattr(*SETTING_MENU_SOUND_FRAME_POS)))
				
				sound_label = normal_title2_gen(sound, SETTING_MENU_SOUND_TITLE, SETTING_MENU_SOUND_TITLE_POS)
				sound.sons.append(sound_label)
				
				volume_music = normal_slider_gen(sound, SETTING_MENU_VOLUME_MUSIC_POS)
				volume_music_label = normal_label_gen(sound, SETTING_MENU_VOLUME_MUSIC_TEXT, SETTING_MENU_VOLUME_MUSIC_LABEL_POS)
				@volume_music.event
				def on_change(val):
					self.volume_music = val
				sound.sons += (volume_music,volume_music_label)
				
				volume_effect = normal_slider_gen(sound, SETTING_MENU_VOLUME_EFFECT_POS)
				volume_effect_label = normal_label_gen(sound, SETTING_MENU_VOLUME_EFFECT_TEXT, SETTING_MENU_VOLUME_EFFECT_LABEL_POS)
				@volume_effect.event
				def on_change(val):
					self.volume_effect = val
				sound.sons += (volume_effect,volume_effect_label)
				
				volume_game = normal_slider_gen(sound, SETTING_MENU_VOLUME_GAME_POS)
				volume_game_label = normal_label_gen(sound, SETTING_MENU_VOLUME_GAME_TEXT, SETTING_MENU_VOLUME_GAME_LABEL_POS)
				@volume_game.event
				def on_change(val):
					self.volume_game = val
				sound.sons += (volume_game,volume_game_label)
				
				setting_menu.sons.append(sound)
				
				fullscreen = normal_checkbox_gen(setting_menu,SETTING_MENU_FULLSCREEN_POS)
				fullscreen_label = normal_label_gen(setting_menu, SETTING_MENU_FULLSCREEN_TEXT, SETTING_MENU_FULLSCREEN_LABEL_POS)
				@fullscreen.event
				def on_press():
					fullscreen.stage ^= 1
				@fullscreen.event
				def on_switch(val):
					self.fullscreen = bool(val)
				
				setting_menu.sons += (fullscreen, fullscreen_label)
				
				@setting_menu.event
				def on_show():
					volume_music._set_rate(self.volume_music)
					volume_effect._set_rate(self.volume_effect)
					volume_game._set_rate(self.volume_game)
					fullscreen._set_stage(int(window.fullscreen))
				
				@setting_menu.event
				def on_submit():
					remove_control(setting_menu)
				return setting_menu
			setting_menu = build_setting_menu()
			push_control(setting_menu)
		
		# 确认退出框
		def show_confirm_quit():
			def build_confirm_quit():
				confirm_quit = MessageBox((window,root,Posattr(*CONFIRM_QUIT_POS)),back = Sprite(normal_menu_back),layouter = MessageBox_defaultlayout_gen(TITLE_HEIGHT = 0))
				
				text = normal_message_text_gen(confirm_quit,CONFIRM_QUIT_TEXT)
				confirm_quit.doc = text
				yes = normal_button_gen(confirm_quit,CONFIRM_QUIT_YES_TEXT)
				no = normal_button_gen(confirm_quit,CONFIRM_QUIT_NO_TEXT)
				confirm_quit.buttons = [no, yes]
				
				@confirm_quit.event
				def on_submit(result):
					remove_control(confirm_quit)
					if result == 1:
						pyglet.app.exit()
				return confirm_quit
			confirm_quit = build_confirm_quit()
			push_control(confirm_quit)
		
		# 关于页面
		
		def show_about_page():
			def build_about_page():
				about_page = AlertBox((window,root,Posattr(*ABOUT_PAGE_POS)),
				back = Sprite(normal_menu_back),layouter = AlertBox_defaultlayout_gen(TITLE_PADDING = 50, PADDING = 30, BUTTON_X = (0.5,-95),BUTTON_WIDTH = (0,190)))
				
				title = normal_title_gen(about_page, ABOUT_PAGE_TITLE)
				about_page.title = title
				
				text = normal_formatted_text_gen(about_page,ABOUT_PAGE_TEXT)
				about_page.doc = text
				
				confirm = normal_button_gen(about_page, ABOUT_PAGE_CONFIRM_TEXT)
				about_page.button = confirm
				
				watch_ed = normal_button_gen(about_page,ABOUT_PAGE_WATCH_ED_TEXT, ABOUT_PAGE_WATCH_ED_POS)
				about_page.sons.append(watch_ed)
				
				@watch_ed.event
				def on_press():
					remove_sons(about_page)
					play_media_page(pyglet.resource.media(ED_FILE,streaming = True))
				@about_page.event
				def on_submit():
					remove_control(about_page)
				return about_page
			about_page = build_about_page()
			push_control(about_page)
		
		# 成就
		def show_achievement_page():
			def build_achievement_page():
				achievement_page = MessageInteractor((window,root),back = Sprite(normal_page_back))
				
				achievement_tagpages = TagPages((window,achievement_page),layouter = TagPages_defaultlayoutV_gen(TAG_HEIGHT = ACHIEVEMENT_TAG_HEIGHT, TAG_PADDING = ACHIEVEMENT_TAG_PADDING, TAG_WIDTH = ACHIEVEMENT_TAG_WIDTH, FULL_PAGE = True))
				achievement_page.sons.append(achievement_tagpages)
				
				ACHIEVEMENT_VISIBLE_PAGES = []
				achievement_tagpages_pages = []
				achievement_tagpages_visible_id = {}
				
				ACHIEVEMENT_VISIBLE_ITEMS = []
				achievement_tagpages_items = []
				
				def show_achievement_message(item):
					messagebox = MessageInteractor((window,root,Posattr(*ACHIEVEMENT_MESSAGE_POS)),back = Sprite(normal_menu_back))
					icon = SpriteControl((window,messagebox,Posattr(*ACHIEVEMENT_MESSAGE_ICON_POS)),Sprite(load_image(item['icon'])))
					title = normal_title_gen(messagebox,item['name'],ACHIEVEMENT_MESSAGE_TITLE_POS)
					label = normal_title2_gen(messagebox,ACHIEVEMENT_MESSAGE_GOTTEN_TITLE if item['gotten'] else ACHIEVEMENT_MESSAGE_UNGOTTEN_TITLE,ACHIEVEMENT_MESSAGE_STATELABEL_POS)
					text = normal_message_text_gen(messagebox,item['text'] if item['gotten'] else item['cond'],ACHIEVEMENT_MESSAGE_TEXT_POS)
					confirm = normal_button_gen(messagebox,ACHIEVEMENT_MESSAGE_CONFIRM_TEXT,ACHIEVEMENT_MESSAGE_CONFIRM_POS)
					messagebox.sons = (icon,title,label,text,confirm)
					messagebox.submit_key = (confirm,'on_press')
					@messagebox.event
					def on_submit():
						remove_control(messagebox)
					push_control(messagebox)
				
				def achievement_tagpage_page_gen(item):
					button = normal_tag_rv_gen(achievement_tagpages,item['name'])
					page = ImageFrame((window,achievement_tagpages,Posattr(*item['pos'])),back = Sprite(load_image(item['background'])))
					return (button, page)
				
				def achievement_tagpage_item_gen(item):
					icon = load_image(item['icon'])
					r = Button((window,achievement_tagpages_pages[achievement_tagpages_visible_id[item['page']]][1],Posattr(*item['pos'])),image = Sprite(icon),hover_color = NORMAL_BUTTON_HOVER_COLOR if item['gotten'] else ACHIEVEMENT_PAGE_ITEM_UNGOTTEN_HOVER_COLOR,
					color = NORMAL_BUTTON_COLOR if item['gotten'] else ACHIEVEMENT_PAGE_ITEM_UNGOTTEN_COLOR)
					@r.event
					def on_press():
						remove_sons(achievement_page)
						show_achievement_message(item)
					return r
				
				def build_achievement_list():
					ACHIEVEMENT_VISIBLE_ITEMS.clear()
					ACHIEVEMENT_VISIBLE_PAGES.clear()
					achievement_tagpages_pages.clear()
					achievement_tagpages_visible_id.clear()
					achievement_tagpages_items.clear()
					for (ky,value) in ACHIEVEMENT_PAGES.items():
						if ACHIEVEMENT_PAGES_DATA.get(ky,{}).get('visible',False):
							ACHIEVEMENT_VISIBLE_PAGES.append(value)
							achievement_tagpages_visible_id[ky]=len(ACHIEVEMENT_VISIBLE_PAGES)-1
					achievement_tagpages_pages.extend([
						achievement_tagpage_page_gen(i)
						for i in ACHIEVEMENT_VISIBLE_PAGES
					])
					achievement_tagpages.pages = achievement_tagpages_pages
					for (ky,value) in ACHIEVEMENT_ITEMS.items():
						if ACHIEVEMENT_DATA.get(ky,{}).get('visible',False) and ACHIEVEMENT_PAGES_DATA.get(value.get('page'),{}).get('visible',False):
							ACHIEVEMENT_VISIBLE_ITEMS.append(value)
							ACHIEVEMENT_VISIBLE_ITEMS[-1]['gotten'] = ACHIEVEMENT_DATA.get(ky,{}).get('gotten',False)
					achievement_tagpages_items.extend([
						achievement_tagpage_item_gen(i)
						for i in ACHIEVEMENT_VISIBLE_ITEMS
					])
					for i in achievement_tagpages_items:
						i.parent.sons.append(i)
					
				achievement_page_title = normal_title0_gen(achievement_page,ACHIEVEMENT_PAGE_TITLE,ACHIEVEMENT_PAGE_TITLE_POS)
				achievement_page.sons.append(achievement_page_title)
				
				achievement_page_confirm = normal_button_gen(achievement_page,ACHIEVEMENT_PAGE_CONFIRM_TEXT,ACHIEVEMENT_PAGE_CONFIRM_POS)
				achievement_page.sons.append(achievement_page_confirm)
				achievement_page.submit_key = (achievement_page_confirm,'on_press')
					
				@achievement_page.event
				def on_show():
					build_achievement_list()
					achievement_tagpages.page = 0
					achievement_page.on_resize()
					
				@achievement_page.event
				def on_submit():
					remove_control(achievement_page)
				return achievement_page
			achievement_page = build_achievement_page()
			push_control(achievement_page)
		# 附录（图鉴）
		
		def show_appendice_page():
			def build_appendice_page():
				appendice_page = MessageInteractor((window,root),back = Sprite(normal_page_back))
				
				title = normal_title0_gen(appendice_page,APPENDICE_PAGE_TITLE, APPENDICE_PAGE_TITLE_POS)
				appendice_page.sons.append(title)
				
				confirm = normal_button_gen(appendice_page,APPENDICE_PAGE_CONFIRM_TEXT,APPENDICE_PAGE_CONFIRM_POS)
				appendice_page.sons.append(confirm)
				appendice_page.submit_key = (confirm,'on_press')
				
				info = ImageFrame((window,appendice_page,Posattr(*APPENDICE_PAGE_INFO_POS)),back = Sprite(normal_menu_back))
				info_icon = SpriteControl((window,info,Posattr(*APPENDICE_PAGE_INFO_ICON_POS)),None)
				info_label = normal_title2_gen(info, '',APPENDICE_PAGE_INFO_LABEL_POS)
				info_text = normal_scrollformattedtext_gen(info,'',APPENDICE_PAGE_INFO_TEXT_POS)
				info.sons += (info_icon, info_label, info_text)
				
				appendice_page.sons.append(info)
				
				select = ImageFrame((window,appendice_page,Posattr(*APPENDICE_PAGE_SELECT_POS)),back = Sprite(normal_menu_back))
				select_scroll = normal_scrollbar_gen(select,APPENDICE_PAGE_SELECT_SCROLL_POS)
				select_list = Viewport((window,select,Posattr(*APPENDICE_PAGE_SELECT_LIST_POS)))
				select.sons += (select_list, select_scroll)
				
				select_list_buttons = SelectButtons((window,select_list),layouter = Grid_defaultlayout_gen(ITEM_HEIGHT = APPENDICE_PAGE_SELECT_ITEM_HEIGHT, ITEM_BLANKING = APPENDICE_PAGE_SELECT_ITEM_BLANKING, PADDING = 0))
				select_list.sons.append(select_list_buttons)
				
				def select_list_items_gen(item):
					r = normal_switchbutton_gen(select_list_buttons,item['name'])
					icon = Sprite(load_image(item['icon']))
					r.icons = [icon,icon]
					return r
				
				APPENDICE_VISIBLE_ITEMS = []
				select_list_items = []
				
				def build_select_list():
					APPENDICE_VISIBLE_ITEMS.clear()
					for (ky,value) in APPENDICE_ITEMS.items():
						if APPENDICE_DATA.get(ky,{}).get('visible',False):
							APPENDICE_VISIBLE_ITEMS.append(value)
					select_list_items.clear()
					select_list_items.extend([
						select_list_items_gen(i)
						for i in APPENDICE_VISIBLE_ITEMS
					])
					select_list_buttons.buttons = select_list_items
					select_list_buttons.absheight = len(select_list_items)*(APPENDICE_PAGE_SELECT_ITEM_HEIGHT+APPENDICE_PAGE_SELECT_ITEM_BLANKING)
				
				@select_list_buttons.event
				def on_switch(id):
					if id < len(APPENDICE_VISIBLE_ITEMS):
						info_icon.image = Sprite(load_image(APPENDICE_VISIBLE_ITEMS[id]['image']))
						info_label.text = APPENDICE_VISIBLE_ITEMS[id]['name']
						info_text.doc.doc = decode_text(APPENDICE_VISIBLE_ITEMS[id]['text'])
					else:
						info_icon.image = None
						info_label.text = ''
						info_text.doc.doc = decode_text(APPENDICE_ITEMS_NONE_TEXT)
					info_text.scrollbar.rate = 0
					info.on_resize()
				
				def select_list_setbase(rate):
					d = select_list.height - select_list_buttons.height
					if d >= 0:
						select_list.y_base = d
					else:
						select_list.y_base = d*rate
				
				@select_list.event
				def on_view_resize():
					select_list_setbase(1-select_scroll.rate)
				@select_scroll.event
				def on_change(rate):
					select_list_setbase(1-rate)
				
				appendice_page.sons.append(select)
				
				@appendice_page.event
				def on_show():
					build_select_list()
					select_scroll.rate = 0
					select_list_buttons.button = 0
					appendice_page.on_resize()
					if len(APPENDICE_VISIBLE_ITEMS)==0:
						alert_notitle(APPENDICE_ITEMS_NONE_TEXT)
					
				@appendice_page.event
				def on_submit():
					remove_control(appendice_page)
				return appendice_page
			appendice_page = build_appendice_page()
			push_control(appendice_page)
		
		# 主菜单
		def show_main_menu():
			def build_main_menu():
				main_menu = ImageFrame((window,root),back = Sprite(load_image(MAIN_MENU_BACK)))

				start_button = Button(
					(window,main_menu,Posattr(*MAIN_MENU_START_POS)),
					label = pyglet.text.Label(MAIN_MENU_START_TEXT,font_name = MAIN_MENU_START_FONT,font_size = MAIN_MENU_START_FONT_SIZE,color = MAIN_MENU_START_COLOR,anchor_x = 'center',anchor_y = 'center'),
					image = Sprite(load_image(MAIN_MENU_START_BACK)),
					pressed_image = Sprite(load_image(MAIN_MENU_START_PRESSED_BACK)),
					hover_color = NORMAL_BUTTON_HOVER_COLOR,
					color = NORMAL_BUTTON_COLOR
				)
				main_menu.sons.append(start_button)
				
				def button_draw(self, event):
					def f(*args, **kw):
						if self.label is not None:
							self.label.font_name = MAIN_MENU_BUTTON_HOVERING_FONT if self.hovering else MAIN_MENU_BUTTON_FONT
						return event(*args, **kw)
					return f
				
				button_gen = lambda pos,text:Button(
					(window,main_menu,Posattr(*pos)),
					label = pyglet.text.Label(text,font_name = MAIN_MENU_BUTTON_FONT,font_size = MAIN_MENU_BUTTON_FONT_SIZE,color = MAIN_MENU_BUTTON_COLOR, anchor_x = 'center',anchor_y = 'center')
				)
				
				load_button =  button_gen(MAIN_MENU_LOAD_POS,MAIN_MENU_LOAD_TEXT)
				load_button.draw = button_draw(load_button, load_button.draw)
				main_menu.sons.append(load_button)
				
				achievement_button = button_gen(MAIN_MENU_ACHIEVEMENT_POS,MAIN_MENU_ACHIEVEMENT_TEXT)
				achievement_button.draw = button_draw(achievement_button, achievement_button.draw)
				main_menu.sons.append(achievement_button)
				
				appendice_button = button_gen(MAIN_MENU_APPENDICE_POS,MAIN_MENU_APPENDICE_TEXT)
				appendice_button.draw = button_draw(appendice_button, appendice_button.draw)
				main_menu.sons.append(appendice_button)
				
				setting_button = button_gen(MAIN_MENU_SETTING_POS,MAIN_MENU_SETTING_TEXT)
				setting_button.draw = button_draw(setting_button, setting_button.draw)
				main_menu.sons.append(setting_button)
				
				about_button = button_gen(MAIN_MENU_ABOUT_POS,MAIN_MENU_ABOUT_TEXT)
				about_button.draw = button_draw(about_button, about_button.draw)
				main_menu.sons.append(about_button)
				
				quit_button = button_gen(MAIN_MENU_QUIT_POS,MAIN_MENU_QUIT_TEXT)
				quit_button.draw = button_draw(quit_button, quit_button.draw)
				main_menu.sons.append(quit_button)
				
				@achievement_button.event
				def on_press():
					remove_sons(main_menu)
					show_achievement_page()
				
				@appendice_button.event
				def on_press():
					remove_sons(main_menu)
					show_appendice_page()
				
				@setting_button.event
				def on_press():
					remove_sons(main_menu)
					show_setting_menu()
				
				@about_button.event
				def on_press():
					remove_sons(main_menu)
					show_about_page()
					
				@quit_button.event
				def on_press():
					remove_sons(main_menu)
					show_confirm_quit()
				return main_menu
				
			main_menu = build_main_menu()
			push_control(main_menu)
			
		@window.event
		def on_resize(width, height):
			root.width = width
			root.height = height
			root.on_resize()
		
		@window.event
		def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
		# 覆盖系统事件，不加这个会很卡
			pass
		
		show_main_menu()
		
		if _DEBUG:
			# FPS(DEBUG)
			fps_display = pyglet.clock.ClockDisplay()
			def window_on_draw():
				window.clear()
				root.draw()
				fps_display.draw()
			window.on_draw = window_on_draw
		
		self.__dict__.update(locals())
	def set_fullscreen(self,v):
		self.window.set_fullscreen(v)
		global FULLSCREEN
		FULLSCREEN = v
	fullscreen = property(lambda self:self.window.fullscreen,set_fullscreen)
	def set_volume_music(self,v):
		self._volume_music = v
		global VOLUME_MUSIC
		VOLUME_MUSIC = v
		# update_volume
	volume_music = property(lambda self:self._volume_music,set_volume_music)
	def set_volume_effect(self,v):
		self._volume_effect = v
		global VOLUME_EFFECT
		VOLUME_EFFECT = v
		# update volume
	volume_effect = property(lambda self:self._volume_effect,set_volume_effect)
	def set_volume_game(self,v):
		self._volume_game = v
		global VOLUME_GAME
		VOLUME_GAME = v
		# update volume
	volume_game = property(lambda self:self._volume_game,set_volume_game)
	def save_settings(self):
		writefile(os.path.join('define','usersettings.py'),str(get_settings()))
	def reset_settings(self):
		writefile(os.path.join('define','usersettings.py'),'{}')
	def run(self):
		self.window.show()
		return pyglet.app.run()

game = GameObject()
game.run()