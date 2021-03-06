#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
import pyglet

from .controls import *
from .data import data, saves
from .uidata import *
from . import uiresource
from . import game

class UI(pyglet.event.EventDispatcher):
	# 用户界面（单类）
	def init_settings(self):
		self.fullscreen = data.get(['FULLSCREEN'])
		self.volume_music = data.get(['VOLUME_MUSIC'])
		self.volume_effect = data.get(['VOLUME_EFFECT'])
		self.volume_game = data.get(['VOLUME_GAME'])
	def reset_settings(self):
		self.fullscreen = data.get(['FULLSCREEN_DEFAULT'])
		self.volume_music = data.get(['VOLUME_MUSIC_DEFAULT'])
		self.volume_effect = data.get(['VOLUME_EFFECT_DEFAULT'])
		self.volume_game = data.get(['VOLUME_GAME_DEFAULT'])
	def set_fullscreen(self,v):
		self.window.set_fullscreen(v)
		data.set(['FULLSCREEN'],v)
	fullscreen = property(lambda self:self.window.fullscreen,set_fullscreen)
	def set_volume_music(self,v):
		self._volume_music = v
		data.set(['VOLUME_MUSIC'],v)
	volume_music = property(lambda self:self._volume_music,set_volume_music)
	def set_volume_effect(self,v):
		self._volume_effect = v
		data.set(['VOLUME_EFFECT'],v)
		# update volume
	volume_effect = property(lambda self:self._volume_effect,set_volume_effect)
	def set_volume_game(self,v):
		self._volume_game = v
		data.set(['VOLUME_GAME'],v)
		# update volume
	volume_game = property(lambda self:self._volume_game,set_volume_game)
	def show(self):
		self.window.show()
	def init(self):
		uiresource.init()
		globals().update(uiresource.vars)
		
		window = Form(960,540,caption = CAPTION,resizable = True)
		self.window = window
		window.set_fullscreen(self.fullscreen)
		window.set_icon(resource.load_static_image(ICON))
		window.set_minimum_size(*MIN_SIZE)
		window.set_mouse_cursor(pyglet.window.ImageMouseCursor(resource.load_static_image(MOUSE_CURSOR), 0, 0))
		
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
		
		# 初始化设置
		
		self.init_settings()
		
		class Middle_Posattr(Posattr):
			def __init__(self):
				super().__init__((0.5,0),(0.5,0),(0,0),(0,0))
		class Normal_ButtonLabel(pyglet.text.Label):
			def __init__(self, text):
				super().__init__(text,font_name = NORMAL_BUTTON_FONT,font_size = NORMAL_BUTTON_FONT_SIZE,color = NORMAL_BUTTON_FONT_COLOR,anchor_x = 'center',anchor_y = 'center')
		class Normal_ValueLabel(pyglet.text.Label):
			def __init__(self, text):
				super().__init__(text,font_name = NORMAL_VALUE_FONT,font_size = NORMAL_VALUE_FONT_SIZE,color = NORMAL_VALUE_FONT_COLOR,anchor_x = 'center',anchor_y = 'center')
		class Normal_Title0(Label):
			def __init__(self,text,pos = DEFAULT_POS):
				super().__init__((window,Posattr(*pos)),pyglet.text.Label(text,font_name = NORMAL_TITLE0_FONT,font_size = NORMAL_TITLE0_FONT_SIZE,color = NORMAL_TITLE0_COLOR, anchor_x = 'center',anchor_y = 'center'))
		class Normal_Title(Label):
			def __init__(self,text,pos = DEFAULT_POS):
				super().__init__((window,Posattr(*pos)),pyglet.text.Label(text,font_name = NORMAL_TITLE_FONT,font_size = NORMAL_TITLE_FONT_SIZE,color = NORMAL_TITLE_COLOR, anchor_x = 'center',anchor_y = 'center'))
		class Normal_Title2(Label):
			def __init__(self,text,pos = DEFAULT_POS):
				super().__init__((window,Posattr(*pos)),pyglet.text.Label(text,font_name = NORMAL_TITLE2_FONT,font_size = NORMAL_TITLE2_FONT_SIZE,color = NORMAL_TITLE2_COLOR, anchor_x = 'center',anchor_y = 'center'))
		class Normal_Label(Label):
			def __init__(self,text,pos = DEFAULT_POS, anchor_x = 'left'):
				super().__init__((window,Posattr(*pos)),pyglet.text.Label(text,font_name = NORMAL_LABEL_FONT,font_size = NORMAL_LABEL_FONT_SIZE,color = NORMAL_LABEL_COLOR, anchor_x = anchor_x,anchor_y = 'center'))
		class Normal_MessageText(TextBox):
			def __init__(self,text,pos = DEFAULT_POS):
				super().__init__((window,Posattr(*pos)),text,NORMAL_MESSAGE_TEXT_STYLE,multiline = True)
		class Normal_TextInput(TextBox):
			def __init__(self, text, pos = DEFAULT_POS):
				super().__init__((window, Posattr(*pos)),text,NORMAL_INPUT_TEXT_STYLE,editable = True,multiline = False,select_backcolor = NORMAL_INPUT_TEXT_SELECT_BACKCOLOR, select_textcolor = NORMAL_INPUT_TEXT_SELECT_TEXTCOLOR, caret_color = NORMAL_INPUT_TEXT_SELECT_CARETCOLOR)
		class Normal_Button(Button):
			def __init__(self, labeltext, pos = DEFAULT_POS):
				super().__init__(
					(window,Posattr(*pos)),
					label = Normal_ButtonLabel(labeltext),
					image = Sprite(normal_button_back),
					pressed_image = Sprite(normal_button_pressed_back),
					hover_color = NORMAL_BUTTON_HOVER_COLOR,
					color = NORMAL_BUTTON_COLOR
				)
		class Normal_Slider(Slider):
			def __init__(self, pos = DEFAULT_POS):
				super().__init__(
					(window,Posattr(*pos)),
					image = Sprite(normal_slider_back),
					cursor = Sprite(normal_slider_cursor)
				)
		class Normal_Checkbox(SwitchButton):
			def __init__(self, pos = DEFAULT_POS):
				super().__init__(
					(window, Posattr(*pos)),
					images = (
						Sprite(normal_checkbox_unchecked_back),
						Sprite(normal_checkbox_checked_back)
					),
					hover_color = NORMAL_BUTTON_HOVER_COLOR,
					color = NORMAL_BUTTON_COLOR
				)
		class Normal_FormattedText(FormattedTextBox):
			def __init__(self, text,pos = DEFAULT_POS):
				super().__init__((window,Posattr(*pos)),resource.decode_text(text),multiline = True)
		class Normal_ScrollBar(ScrollBar):
			def __init__(self, pos = DEFAULT_POS):
				super().__init__((window,Posattr(*pos)), image = Sprite(normal_scrollbar_back), cursor = Sprite(normal_scrollbar_cursor))
		class Normal_SwitchButton(SwitchButton):
			def __init__(self,text,pos = DEFAULT_POS):
				title = Normal_ButtonLabel(text)
				super().__init__(
					(window,pos),
					[title,title],
					[Sprite(normal_switchbutton_back),Sprite(normal_switchbutton_select_back)],
					hover_color = NORMAL_BUTTON_HOVER_COLOR,
					color = NORMAL_BUTTON_COLOR
				)
		class Normal_Tag_rv(SwitchButton):
			def __init__(self, text,pos = DEFAULT_POS):
				title = Normal_ButtonLabel(text)
				super().__init__(
					(window,pos),
					[title,title],
					[Sprite(normal_tag_rv_back),Sprite(normal_tag_rv_selected_back)],
					hover_color = NORMAL_BUTTON_HOVER_COLOR,
					color = NORMAL_BUTTON_COLOR
				)
		class Normal_ScrollText(ScrollTextBox):
			def __init__(self,text,pos = DEFAULT_POS):
				super().__init__((window,Posattr(*pos)))
				doc = Normal_MessageText(text)
				scrollbar = Normal_ScrollBar()
				self.doc = doc
				self.scrollbar = scrollbar
		class Normal_ScrollFormattedText(ScrollTextBox):
			def __init__(self,text,pos = DEFAULT_POS):
				super().__init__((window,Posattr(*pos)))
				doc = Normal_FormattedText(text)
				scrollbar = Normal_ScrollBar()
				self.doc = doc
				self.scrollbar = scrollbar
						
		# 对 UI 特化的控件类，用于UI中的独立界面
		# 不符合替换原则
		class UIControl(object):
			def exe(self):
				# 执行该控件
				self.refresh()
				push_control(self)
			def end(self):
				remove_control(self)
			def refresh(self):
				# 刷新数据
				pass
		class Alert(AlertBox,UIControl):
			def __init__(self, text, title, pos = NORMAL_ALERT_POS):
				super().__init__((window,Posattr(*pos)),back = Sprite(normal_menu_back),layouter = AlertBox_defaultlayout_gen())
				alert_text = Normal_MessageText(text)
				self.doc = alert_text
				alert_title = Normal_Title(title)
				self.title = alert_title
				alert_button = Normal_Button(NORMAL_ALERT_BUTTON_TEXT)
				self.button = alert_button
				@self.event
				def on_submit():
					self.end()
		class Alert_Notitle(AlertBox,UIControl):
			def __init__(self, text, pos = NORMAL_ALERT_NOTITLE_POS):
				super().__init__((window,Posattr(*pos)),back = Sprite(normal_menu_back),layouter = AlertBox_defaultlayout_gen(TITLE_HEIGHT = 0))
				alert_text = Normal_MessageText(text)
				self.doc = alert_text
				alert_button = Normal_Button(NORMAL_ALERT_BUTTON_TEXT)
				self.button = alert_button
				@self.event
				def on_submit():
					self.end()
		class MediaPage(MediaPlayer,UIControl):
			def __init__(self, media, loop = False):
				super().__init__([window])
				self.player = pyglet.media.player.Player()
				self.queue(media)
				self.loop = loop
				self.play()
				@self.event
				def on_eos():
					self.end()
				@self.event
				def on_press(*args,**kw):
					self.end()
			def end(self):
				self.clear()
				UIControl.end(self)
		class MessageWindow(AlertBox,UIControl):
			def __init__(self, text, title, image = None, pos = None):
				if pos is None:
					pos = NORMAL_MESSAGE_POS
				if image is None:
					image = Sprite(normal_message_back)
				super().__init__((window,Posattr(*pos)),back = image,layouter = AlertBox_defaultlayout_gen())
				alert_text = Normal_MessageText(text)
				self.doc = alert_text
				alert_title = Normal_Title(title)
				self.title = alert_title
				alert_button = Normal_Button(NORMAL_MESSAGE_BUTTON_TEXT)
				self.button = alert_button
				@self.event
				def on_submit():
					self.end()
				
		# 设置菜单
		class SettingMenu(MessageInteractor,UIControl):
			def __init__(self):
				super().__init__((window,Posattr(*SETTING_MENU_POS)),back = Sprite(normal_menu_back))
				
				title = Normal_Title(SETTING_MENU_TITLE, SETTING_MENU_TITLE_POS)
				self.sons.append(title)
				self.title = title
				
				confirm = Normal_Button(SETTING_MENU_CONFIRM_TEXT,SETTING_MENU_CONFIRM_POS)
				self.sons.append(confirm)
				self.confirm = confirm
				self.submit_key = (confirm,'on_press')
				
				reset = Normal_Button(SETTING_MENU_RESET_TEXT,SETTING_MENU_RESET_POS)
				self.sons.append(reset)
				self.reset = reset
				
				sound = Frame((window,Posattr(*SETTING_MENU_SOUND_FRAME_POS)))
				self.sons.append(sound)
				self.sound = sound
				
				sound_label = Normal_Title2(SETTING_MENU_SOUND_TITLE, SETTING_MENU_SOUND_TITLE_POS)
				sound.sons.append(sound_label)
				self.sound_label = sound_label
				
				volume_music = Normal_Slider(SETTING_MENU_VOLUME_MUSIC_POS)
				volume_music_label = Normal_Label(SETTING_MENU_VOLUME_MUSIC_TEXT, SETTING_MENU_VOLUME_MUSIC_LABEL_POS)
				sound.sons += (volume_music,volume_music_label)
				self.volume_music = volume_music
				self.volume_music_label = volume_music_label
				
				volume_effect = Normal_Slider(SETTING_MENU_VOLUME_EFFECT_POS)
				volume_effect_label = Normal_Label(SETTING_MENU_VOLUME_EFFECT_TEXT, SETTING_MENU_VOLUME_EFFECT_LABEL_POS)
				sound.sons += (volume_effect,volume_effect_label)
				self.volume_effect = volume_effect
				self.volume_effect_label = volume_effect_label
				
				volume_game = Normal_Slider(SETTING_MENU_VOLUME_GAME_POS)
				volume_game_label = Normal_Label(SETTING_MENU_VOLUME_GAME_TEXT, SETTING_MENU_VOLUME_GAME_LABEL_POS)
				
				sound.sons += (volume_game,volume_game_label)
				self.volume_game = volume_game
				self.volume_game_label = volume_game_label
				
				fullscreen = Normal_Checkbox(SETTING_MENU_FULLSCREEN_POS)
				fullscreen_label = Normal_Label(SETTING_MENU_FULLSCREEN_TEXT, SETTING_MENU_FULLSCREEN_LABEL_POS)
				
				self.sons += (fullscreen, fullscreen_label)
				self.fullscreen = fullscreen
				self.fullscreen_label = fullscreen_label
				
				@reset.event
				def on_press():
					ui.reset_settings()
					self.refresh()
				@volume_music.event
				def on_change(val):
					ui.volume_music = val
				@volume_effect.event
				def on_change(val):
					ui.volume_effect = val
				@volume_game.event
				def on_change(val):
					ui.volume_game = val
				@fullscreen.event
				def on_press():
					fullscreen.stage ^= 1
				@fullscreen.event
				def on_switch(val):
					ui.fullscreen = bool(val)
				@self.event
				def on_show():
					self.refresh()
				@self.event
				def on_submit():
					self.end()
			def refresh(self):
				self.volume_music._set_rate(ui.volume_music)
				self.volume_effect._set_rate(ui.volume_effect)
				self.volume_game._set_rate(ui.volume_game)
				self.fullscreen._set_stage(int(window.fullscreen))
		
		# 确认框
		class ConfirmBox(MessageBox,UIControl):
			def __init__(self, text, pos = CONFIRM_BOX_POS):
				super().__init__((window,Posattr(*pos)),back = Sprite(normal_menu_back),layouter = MessageBox_defaultlayout_gen(TITLE_HEIGHT = 0))
				
				text = Normal_MessageText(text)
				self.doc = text
				yes = Normal_Button(CONFIRM_BOX_YES_TEXT)
				no = Normal_Button(CONFIRM_BOX_NO_TEXT)
				self.buttons = [no, yes]
				
				@self.event
				def on_submit(result):
					remove_control(self)
					if result == 1:
						pyglet.app.exit()
		# 版本信息
		class VersionPage(AlertBox,UIControl):
			def __init__(self):
				text = data.version.checksum_to_str() + '\n\n' + data.version.name_to_str()
				super().__init__((window,Posattr(*VERSION_PAGE_POS)),back = Sprite(normal_menu_back),layouter = AlertBox_defaultlayout_gen())
				alert_text = Normal_ScrollText(text)
				self.doc = alert_text
				alert_title = Normal_Title(VERSION_PAGE_TITLE)
				self.title = alert_title
				alert_button = Normal_Button(NORMAL_ALERT_BUTTON_TEXT)
				self.button = alert_button
				@self.event
				def on_submit():
					self.end()
		# 关于页面
		class AboutPage(AlertBox,UIControl):
			def __init__(self):
				super().__init__((window,Posattr(*ABOUT_PAGE_POS)),
				back = Sprite(normal_menu_back),layouter = AlertBox_defaultlayout_gen(TITLE_PADDING = 50, PADDING = 30, BUTTON_X = (0.5,-95),BUTTON_WIDTH = (0,190)))
				
				title = Normal_Title(ABOUT_PAGE_TITLE)
				self.title = title
				
				text = Normal_FormattedText(ABOUT_PAGE_TEXT)
				self.doc = text
				
				confirm = Normal_Button(ABOUT_PAGE_CONFIRM_TEXT)
				self.button = confirm
				
				watch_ed = Normal_Button(ABOUT_PAGE_WATCH_ED_TEXT, ABOUT_PAGE_WATCH_ED_POS)
				self.sons.append(watch_ed)
				
				show_version_page = Normal_Button(ABOUT_PAGE_SHOW_VERSION_PAGE_TEXT,ABOUT_PAGE_SHOW_VERSION_PAGE_POS)
				self.sons.append(show_version_page)
				
				@show_version_page.event
				def on_press():
					remove_sons(self)
					VersionPage().exe()
				@watch_ed.event
				def on_press():
					remove_sons(self)
					MediaPage(pyglet.resource.media(ED_FILE,streaming = True)).exe()
				@self.event
				def on_submit():
					self.end()
		
		# 成就的UI数据
		class AchievementItem_UIData(UIData_DictItem):
			def build_control(self):
				icon = resource.load_image(self.icon)
				self.icon_control = SpriteControl((window,Posattr(*ACHIEVEMENT_MESSAGE_ICON_POS)),Sprite(icon))
				return Button((window,Posattr(*self.pos)),image = Sprite(icon))
		class AchievementItems_UIData(UIDataStaticSet):
			_built_dataset = False
			_data = data.get_all_dict(['ACHIEVEMENT_ITEMS'])
			@classmethod
			def build_dataset(cls):
				return {item[0]:AchievementItem_UIData(item) for item in cls._data.items()}
		# 成就页的UI数据
		class AchievementPage_UIData(UIData_DictItem):
			def build_control(self):
				return Normal_Tag_rv(self.name), ImageFrame((window,Posattr(*self.pos)),back = Sprite(resource.load_image(self.background)))
		class AchievementPages_UIData(UIDataStaticSet):
			_built_dataset = False
			_data = data.get_all_dict(['ACHIEVEMENT_PAGES'])
			@classmethod
			def build_dataset(cls):
				return {item[0]:AchievementPage_UIData(item) for item in cls._data.items()}
		class AchievementPage_Pages(object):
			# 生成页面。由于成就页面的特性，还绑定了事件
			@staticmethod
			def get(parent_page):
				achievement_items = AchievementItems_UIData.dataset()
				achievement_pages = AchievementPages_UIData.dataset()
				
				ACHIEVEMENT_PAGES_DATA = data.get_all_dict(['ACHIEVEMENT_PAGES_DATA'])
				ACHIEVEMENT_DATA = data.get_all_dict(['ACHIEVEMENT_DATA'])
				def check_page_visible(page):
					return ACHIEVEMENT_PAGES_DATA.get(page,{}).get('visible',False)
				def check_item_visible(item):
					return ACHIEVEMENT_DATA.get(item,{}).get('visible',False)
				def check_item_got(item):
					return ACHIEVEMENT_DATA.get(item,{}).get('got',False)
				
				pages = []
				for key,value in achievement_pages.items():
					if check_page_visible(key):
						pages.append(value.control)
						value.control[1].sons.clear()
				for key,value in achievement_items.items():
					if check_item_visible(key):
						if check_page_visible(value.page):
							achievement_pages[value.page].control[1].sons.append(value.control)
							got = check_item_got(key)
							value.control.hover_color = NORMAL_BUTTON_HOVER_COLOR if got else ACHIEVEMENT_PAGE_ITEM_UNGOTTEN_HOVER_COLOR
							value.control.color = NORMAL_BUTTON_COLOR if got else ACHIEVEMENT_PAGE_ITEM_UNGOTTEN_COLOR
							def get_event(value, got):
								def on_press():
									remove_sons(parent_page)
									AchievementMessage(value, got).exe()
								return on_press
							value.control.on_press = get_event(value, got)
				return pages
		# 成就信息
		class AchievementMessage(MessageInteractor,UIControl):
			def __init__(self, item, got):
				super().__init__((window,Posattr(*ACHIEVEMENT_MESSAGE_POS)),back = Sprite(normal_menu_back))
				icon = item.icon_control
				title = Normal_Title(item.name,ACHIEVEMENT_MESSAGE_TITLE_POS)
				label = Normal_Title2(ACHIEVEMENT_MESSAGE_GOTTEN_TITLE if got else ACHIEVEMENT_MESSAGE_UNGOTTEN_TITLE,ACHIEVEMENT_MESSAGE_STATELABEL_POS)
				text = Normal_MessageText(item.text if got else item.cond,ACHIEVEMENT_MESSAGE_TEXT_POS)
				confirm = Normal_Button(ACHIEVEMENT_MESSAGE_CONFIRM_TEXT,ACHIEVEMENT_MESSAGE_CONFIRM_POS)
				self.sons = (icon,title,label,text,confirm)
				self.submit_key = (confirm,'on_press')
				@self.event
				def on_submit():
					self.end()
		# 成就
		class AchievementPage(MessageInteractor,UIControl):
			def __init__(self):
				super().__init__([window],back = Sprite(normal_page_back))
				
				achievement_tagpages = TagPages([window],layouter = TagPages_defaultlayoutV_gen(TAG_HEIGHT = ACHIEVEMENT_TAG_HEIGHT, TAG_PADDING = ACHIEVEMENT_TAG_PADDING, TAG_WIDTH = ACHIEVEMENT_TAG_WIDTH, FULL_PAGE = True))
				self.sons.append(achievement_tagpages)
				self.achievement_tagpages = achievement_tagpages
				
				achievement_page_title = Normal_Title0(ACHIEVEMENT_PAGE_TITLE,ACHIEVEMENT_PAGE_TITLE_POS)
				self.sons.append(achievement_page_title)
				self.achievement_page_title = achievement_page_title
				
				achievement_page_confirm = Normal_Button(ACHIEVEMENT_PAGE_CONFIRM_TEXT,ACHIEVEMENT_PAGE_CONFIRM_POS)
				self.sons.append(achievement_page_confirm)
				self.submit_key = (achievement_page_confirm,'on_press')
				self.achievement_page_confirm = achievement_page_confirm
				
				@self.event
				def on_show():
					self.refresh()
				@self.event
				def on_submit():
					self.end()
				
			def refresh(self):
				self.achievement_tagpages.pages = AchievementPage_Pages.get(self)
				self.on_resize()
		class AppendiceItem_UIData(UIData_DictItem):
			def build_control(self):
				r = Normal_SwitchButton(self.name)
				icon = Sprite(resource.load_image(self.icon))
				r.icons = [icon,icon]
				self.image = Sprite(resource.load_image(self.image))
				self.doc = resource.decode_text(self.text)
				return r
		class AppendiceItems_UIData(UIDataStaticSet):
			_built_dataset = False
			_data = data.get_all_dict(['APPENDICE_ITEMS'])
			@classmethod
			def build_dataset(cls):
				return {item[0]:AppendiceItem_UIData(item) for item in cls._data.items()}
		class AppendicePage_Items(object):
			@classmethod
			def get(self):
				appendice_items = AppendiceItems_UIData.dataset()
				APPENDICE_DATA = data.get_all_dict(['APPENDICE_DATA'])
				
				def check_item_visible(item):
					return APPENDICE_DATA.get(item,{}).get('visible',False)
				
				items = []
				items_data = []
				for key,value in appendice_items.items():
					if check_item_visible(key):
						items.append(value.control)
						items_data.append(value)
				return items, items_data
				
		# 附录（图鉴）
		class AppendicePage(MessageInteractor,UIControl):
			def __init__(self):
				super().__init__([window],back = Sprite(normal_page_back))
				
				title = Normal_Title0(APPENDICE_PAGE_TITLE, APPENDICE_PAGE_TITLE_POS)
				self.sons.append(title)
				self.title = title
				
				confirm = Normal_Button(APPENDICE_PAGE_CONFIRM_TEXT,APPENDICE_PAGE_CONFIRM_POS)
				self.sons.append(confirm)
				self.confirm = confirm
				
				info = ImageFrame((window,Posattr(*APPENDICE_PAGE_INFO_POS)),back = Sprite(normal_menu_back))
				self.sons.append(info)
				self.info = info
				info_icon = SpriteControl((window,Posattr(*APPENDICE_PAGE_INFO_ICON_POS)),None)
				info_label = Normal_Title2('',APPENDICE_PAGE_INFO_LABEL_POS)
				info_text = Normal_ScrollFormattedText('',APPENDICE_PAGE_INFO_TEXT_POS)
				info.sons += (info_icon, info_label, info_text)
				self.info_icon = info_icon
				self.info_label = info_label
				self.info_text = info_text
				def info_refresh():
					self.info_text.scrollbar.rate = 0
					self.info.on_resize()
				info.refresh = info_refresh
				
				select = ImageFrame((window,Posattr(*APPENDICE_PAGE_SELECT_POS)),back = Sprite(normal_menu_back))
				self.select = select
				self.sons.append(select)
				select_list = ScrollFrame([window])
				self.select_list = select_list
				select.sons.append(select_list)
				
				select_scroll = Normal_ScrollBar()
				self.select_scroll = select_scroll
				select_list_buttons = SelectButtons([window],layouter = Grid_defaultlayout_gen(ITEM_HEIGHT = APPENDICE_PAGE_SELECT_ITEM_HEIGHT, ITEM_BLANKING = APPENDICE_PAGE_SELECT_ITEM_BLANKING, PADDING = 0))
				self.select_list_buttons = select_list_buttons
				select_list.frame = select_list_buttons
				select_list.scrollbar = select_scroll
				
				self.submit_key = (confirm,'on_press')
				@self.event
				def on_show():
					self.refresh()
					if len(self.select_list_buttons.buttons)==0:
						self.end()
						Alert_Notitle(APPENDICE_ITEMS_NONE_TEXT).exe()
				@self.event
				def on_submit():
					self.end()
			def refresh(self):
				self.select_list_buttons.buttons, items_data = AppendicePage_Items.get()
				@self.select_list_buttons.event
				def on_switch(id):
					if id < len(self.select_list_buttons.buttons):
						self.info_icon.image = items_data[id].image
						self.info_label.text = items_data[id].name
						self.info_text.doc.doc = items_data[id].doc
					else:
						self.info_icon.image = None
						self.info_label.text = ''
						self.info_text.doc.doc = ''
					self.info.refresh()
				self.select_list_buttons.button = 0
				self.on_resize()
		
		class ScenarioItem_UIData(UIData_DictItem):
			def build_control(self):
				r = Normal_SwitchButton(self.name)
				icon = Sprite(resource.load_image(self.icon))
				r.icons = [icon,icon]
				self.image = Sprite(resource.load_image(self.image))
				self.doc = resource.decode_text(self.text)
				return r
		class ScenarioItems_UIData(UIDataStaticSet):
			_built_dataset = False
			_data = data.get_all_dict(['SCENARIOS'])
			@classmethod
			def build_dataset(cls):
				return {item[0]:ScenarioItem_UIData(item) for item in cls._data.items()}
		class ScenarioPage_Items(object):
			@classmethod
			def get(self):
				scenario_items = ScenarioItems_UIData.dataset()
				SCENARIOS_DATA = data.get_all_dict(['SCENARIOS_DATA'])
				
				def check_item_visible(item):
					return SCENARIOS_DATA.get(item,{}).get('visible',False)
				
				items = []
				items_data = []
				for key,value in scenario_items.items():
					if check_item_visible(key):
						items.append(value.control)
						items_data.append(value)
				
				return items, items_data
				
		# 剧本选择-开始游戏页面
		class ScenarioPage(MessageInteractor, UIControl):
			# _items_loaded = False
			def __init__(self):
				super().__init__([window],back = Sprite(normal_page_back))
				
				title = Normal_Title0(SCENARIO_PAGE_TITLE, SCENARIO_PAGE_TITLE_POS)
				self.sons.append(title)
				self.title = title
				
				confirm = Normal_Button(SCENARIO_PAGE_CONFIRM_TEXT,SCENARIO_PAGE_CONFIRM_POS)
				self.sons.append(confirm)
				self.confirm = confirm
				
				start_button = Normal_Button(SCENARIO_PAGE_START_TEXT,SCENARIO_PAGE_START_POS)
				self.sons.append(start_button)
				self.start_button = start_button
				
				info = ImageFrame((window,Posattr(*SCENARIO_PAGE_INFO_POS)),back = Sprite(normal_menu_back))
				info_icon = SpriteControl((window,Posattr(*SCENARIO_PAGE_INFO_ICON_POS)),None)
				info_label = Normal_Title2('',SCENARIO_PAGE_INFO_LABEL_POS)
				info_text = Normal_ScrollFormattedText('',SCENARIO_PAGE_INFO_TEXT_POS)
				info.sons += (info_icon, info_label, info_text)
				self.sons.append(info)
				self.info = info
				self.info_icon = info_icon
				self.info_label = info_label
				self.info_text = info_text
				def info_refresh():
					self.info_text.scrollbar.rate = 0
					self.info.on_resize()
				info.refresh = info_refresh
				
				select = ImageFrame((window,Posattr(*SCENARIO_PAGE_SELECT_POS)),back = Sprite(normal_menu_back))
				self.select = select
				self.sons.append(select)
				select_list = ScrollFrame([window])
				self.select_list = select_list
				select.sons.append(select_list)
				
				select_scroll = Normal_ScrollBar()
				self.select_scroll = select_scroll
				select_list_buttons = SelectButtons([window],layouter = Grid_defaultlayout_gen(ITEM_HEIGHT = SCENARIO_PAGE_SELECT_ITEM_HEIGHT, ITEM_BLANKING = SCENARIO_PAGE_SELECT_ITEM_BLANKING, PADDING = 0))
				self.select_list_buttons = select_list_buttons
				select_list.frame = select_list_buttons
				select_list.scrollbar = select_scroll
				
				@confirm.event
				def on_press():
					self.dispatch_event('on_submit',-1)
				@start_button.event
				def on_press():
					self.dispatch_event('on_submit',select_list_buttons.button)
				@self.event
				def on_show():
					self.refresh()
					if len(self.select_list_buttons.buttons)==0:
						alert_box = Alert_Notitle(SCENARIO_ITEMS_NONE_TEXT)
						@alert_box.event
						def on_submit():
							remove_control(self)
						alert_box.exe()
				@self.event
				def on_submit(id):
					self.end()
					if id != -1:
						scenario = self.items_data[id]
						play_game_from_scenario(scenario)
			def refresh(self):
				self.select_list_buttons.buttons, items_data = ScenarioPage_Items.get()
				self.items_data = items_data
				@self.select_list_buttons.event
				def on_switch(id):
					if id < len(self.select_list_buttons.buttons):
						self.info_icon.image = items_data[id].image
						self.info_label.text = items_data[id].name
						self.info_text.doc.doc = items_data[id].doc
					else:
						self.info_icon.image = None
						self.info_label.text = ''
						self.info_text.doc.doc = ''
					self.info.refresh()
				self.select_list_buttons.button = 0
				self.on_resize()
				
		# 主菜单
		class MainMenu(ImageFrame,UIControl):
			def __init__(self):
				super().__init__([window],back = Sprite(main_menu_back))
				start_button = Button(
					(window,Posattr(*MAIN_MENU_START_POS)),
					label = pyglet.text.Label(MAIN_MENU_START_TEXT,font_name = MAIN_MENU_START_FONT,font_size = MAIN_MENU_START_FONT_SIZE,color = MAIN_MENU_START_COLOR,anchor_x = 'center',anchor_y = 'center'),
					image = Sprite(main_menu_start_back),
					pressed_image = Sprite(main_menu_start_pressed_back),
					hover_color = NORMAL_BUTTON_HOVER_COLOR,
					color = NORMAL_BUTTON_COLOR
				)
				self.sons.append(start_button)
				
				def button_draw(self, event):
					def f(*args, **kw):
						if self.label is not None:
							self.label.font_name = MAIN_MENU_BUTTON_HOVERING_FONT if self.hovering else MAIN_MENU_BUTTON_FONT
						return event(*args, **kw)
					return f
				
				button_gen = lambda pos,text:Button(
					(window,Posattr(*pos)),
					label = pyglet.text.Label(text,font_name = MAIN_MENU_BUTTON_FONT,font_size = MAIN_MENU_BUTTON_FONT_SIZE,color = MAIN_MENU_BUTTON_COLOR, anchor_x = 'center',anchor_y = 'center')
				)
				
				load_button =  button_gen(MAIN_MENU_LOAD_POS,MAIN_MENU_LOAD_TEXT)
				load_button.draw = button_draw(load_button, load_button.draw)
				self.sons.append(load_button)
				
				achievement_button = button_gen(MAIN_MENU_ACHIEVEMENT_POS,MAIN_MENU_ACHIEVEMENT_TEXT)
				achievement_button.draw = button_draw(achievement_button, achievement_button.draw)
				self.sons.append(achievement_button)
				
				appendice_button = button_gen(MAIN_MENU_APPENDICE_POS,MAIN_MENU_APPENDICE_TEXT)
				appendice_button.draw = button_draw(appendice_button, appendice_button.draw)
				self.sons.append(appendice_button)
				
				setting_button = button_gen(MAIN_MENU_SETTING_POS,MAIN_MENU_SETTING_TEXT)
				setting_button.draw = button_draw(setting_button, setting_button.draw)
				self.sons.append(setting_button)
				
				about_button = button_gen(MAIN_MENU_ABOUT_POS,MAIN_MENU_ABOUT_TEXT)
				about_button.draw = button_draw(about_button, about_button.draw)
				self.sons.append(about_button)
				
				quit_button = button_gen(MAIN_MENU_QUIT_POS,MAIN_MENU_QUIT_TEXT)
				quit_button.draw = button_draw(quit_button, quit_button.draw)
				self.sons.append(quit_button)
				
				@start_button.event
				def on_press():
					remove_sons(self)
					ScenarioPage().exe()
				@load_button.event
				def on_press():
					remove_sons(self)
					GamePageLoad().exe()
				@achievement_button.event
				def on_press():
					remove_sons(self)
					AchievementPage().exe()
				@appendice_button.event
				def on_press():
					remove_sons(self)
					AppendicePage().exe()
				@setting_button.event
				def on_press():
					remove_sons(self)
					SettingMenu().exe()
				@about_button.event
				def on_press():
					remove_sons(self)
					AboutPage().exe()
				@quit_button.event
				def on_press():
					remove_sons(self)
					confirm = ConfirmBox(CONFIRM_QUIT_TEXT)
					@confirm.event
					def on_submit(result):
						confirm.end()
						if result == 1:
							pyglet.app.exit()
					confirm.exe()
		class SavesBox(ScrollFrame):
			# 载入、显示及浏览存档
			def __init__(self,  pos = DEFAULT_POS):
				super().__init__((window, Posattr(*pos)))
				
				select_list_buttons = SelectButtons([window],layouter = Grid_defaultlayout_gen(ITEM_HEIGHT = SAVESBOX_SELECT_ITEM_HEIGHT, ITEM_BLANKING = SAVESBOX_SELECT_ITEM_BLANKING, PADDING = 0))
				self.frame = select_list_buttons
				
				scrollbar = Normal_ScrollBar()
				self.scrollbar = scrollbar
			def refresh(self):
				self.SAVES = []
				self.select_list_items = []
				
				def select_list_items_gen(item):
					r = Normal_SwitchButton(item)
					return r
				def build_select_list():
					self.SAVES = saves.get_save_names()
					self.select_list_items = [
						select_list_items_gen(i)
						for i in self.SAVES
					]
					self.frame.buttons = self.select_list_items
					if self.frame.visible:
						self.frame.show()
				@self.frame.event
				def on_switch(id):
					if id < len(self.SAVES):
						self.dispatch_event('on_select_save',self.SAVES[id])
					else:
						self.dispatch_event('on_select_save','')
				build_select_list()
				self.scrollbar.rate = 0
				self.frame.button = 0
				self.on_resize()
		SavesBox.register_event_type('on_select_save')
		class GamePageSave(MessageInteractor, UIControl):
			def __init__(self, gamepage):
				super().__init__((window,Posattr(*SAVEPAGE_POS)), back = Sprite(normal_menu_back))
				self.gamepage = gamepage
				
				title = Normal_Title(SAVEPAGE_TITLE, SAVEPAGE_TITLE_POS)
				self.sons.append(title)
				self.title = title
				
				confirm_button = Normal_Button(SAVEPAGE_CONFIRM_TEXT,SAVEPAGE_CONFIRM_POS)
				self.sons.append(confirm_button)
				self.confirm_button = confirm_button
				
				delete_button = Normal_Button(SAVEPAGE_DEL_TEXT,SAVEPAGE_DEL_POS)
				self.sons.append(delete_button)
				self.delete_button = delete_button
				
				cancel = Normal_Button(SAVEPAGE_CANCEL_TEXT,SAVEPAGE_CANCEL_POS)
				self.sons.append(cancel)
				self.cancel = cancel
				self.submit_key = (cancel,'on_press')
				
				saves_box = SavesBox(SAVEPAGE_SELECT_POS)
				self.sons.append(saves_box)
				self.saves_box = saves_box
				
				name_label = Normal_Label(SAVEPAGE_NAME_LABEL_TEXT, SAVEPAGE_NAME_LABEL_POS)
				name = Normal_TextInput('', SAVEPAGE_NAME_POS)
				self.name_label = name_label
				self.name = name
				self.sons += (name, name_label)
				
				@confirm_button.event
				def on_press():
					remove_sons(self)
					self.confirm()
				@delete_button.event
				def on_press():
					remove_sons(self)
					self.delete()
				@saves_box.event
				def on_select_save(save_name):
					self.save_name = save_name
				@self.event
				def on_show():
					self.refresh()
				@self.event
				def on_submit(*args):
					self.end()
			def refresh(self):
				self.saves_box.refresh()
				self.save_name = saves.get_available_save_name()
			def set_save_name(self, save_name):
				self.name.text = save_name
			def get_save_name(self):
				self.name.text = saves.trans_name(self.name.text)
				return self.name.text
			save_name = property(get_save_name,set_save_name)
			def delete(self):
				if saves.test_save_exists(self.save_name):
					confirm_box = ConfirmBox(SAVEPAGE_DEL_CONFIRM_TEXT)
					@confirm_box.event
					def on_submit(result):
						confirm_box.end()
						if result == 1:
							self.remove()
					confirm_box.exe()
				else:
					Alert_Notitle(SAVEPAGE_DEL_NOTEXIST_TEXT).exe()
			def confirm(self):
				if saves.test_save_exists(self.save_name):
					confirm_box = ConfirmBox(SAVEPAGE_CONFIRM_SAVE_CONFLICT_TEXT)
					@confirm_box.event
					def on_submit(result):
						confirm_box.end()
						if result == 1:
							self.save()
					confirm_box.exe()
				else:
					self.save()
			def remove(self):
				saves.remove(self.save_name)
				self.saves_box.refresh()
			def save(self):
				saves.save(self.save_name, self.gamepage.gameplay.gamedata)
				self.saves_box.refresh()
				self.end()
		class GamePageLoad(MessageInteractor, UIControl):
			def __init__(self):
				super().__init__((window,Posattr(*LOADPAGE_POS)), back = Sprite(normal_menu_back))
				
				title = Normal_Title(LOADPAGE_TITLE, LOADPAGE_TITLE_POS)
				self.sons.append(title)
				self.title = title
				
				confirm_button = Normal_Button(LOADPAGE_CONFIRM_TEXT,LOADPAGE_CONFIRM_POS)
				self.sons.append(confirm_button)
				self.confirm_button = confirm_button
				
				delete_button = Normal_Button(LOADPAGE_DEL_TEXT,LOADPAGE_DEL_POS)
				self.sons.append(delete_button)
				self.delete_button = delete_button
				
				cancel = Normal_Button(LOADPAGE_CANCEL_TEXT,LOADPAGE_CANCEL_POS)
				self.sons.append(cancel)
				self.cancel = cancel
				self.submit_key = (cancel,'on_press')
				
				saves_box = SavesBox(LOADPAGE_SELECT_POS)
				self.sons.append(saves_box)
				self.saves_box = saves_box
				
				checksum_label = Normal_Label(LOADPAGE_CHECKSUM_LABEL_TEXT, LOADPAGE_CHECKSUM_LABEL_POS)
				checksum = Normal_MessageText('', LOADPAGE_CHECKSUM_POS)
				self.checksum_label = checksum_label
				self.checksum = checksum
				self.sons += (checksum, checksum_label)
				
				version_box = Normal_ScrollText('', LOADPAGE_VERSION_POS)
				self.version_box = version_box
				self.sons.append(version_box)
				
				self.save_name = ''
				
				@confirm_button.event
				def on_press():
					remove_sons(self)
					self.confirm()
				@delete_button.event
				def on_press():
					remove_sons(self)
					self.delete()
				@saves_box.event
				def on_select_save(save_name):
					self.save_name = save_name
				@self.event
				def on_show():
					self.refresh()
					if len(self.saves_box.SAVES) == 0:
						self.end()
						Alert_Notitle(LOADPAGE_NONE_TEXT).exe()
				@self.event
				def on_submit(*args):
					self.end()
			def refresh(self):
				self.save_name = ''
				self.save_data = {}
				self.saves_box.refresh()
			def delete(self):
				if saves.test_save_exists(self.save_name):
					confirm_box = ConfirmBox(LOADPAGE_DEL_CONFIRM_TEXT)
					@confirm_box.event
					def on_submit(result):
						confirm_box.end()
						if result == 1:
							self.remove()
					confirm_box.exe()
				else:
					Alert_Notitle(LOADPAGE_NOTEXIST_TEXT).exe()
			def remove(self):				
				saves.remove(self.save_name)
				self.saves_box.refresh()
			def confirm(self):
				if saves.test_save_exists(self.save_name):
					if data.version == self.version:
						self.start_play()
					else:
						confirm_box = ConfirmBox(LOADPAGE_VERSION_CONFIRM_TEXT,CONFIRM_BOX_POS_MIDDLE)
						@confirm_box.event
						def on_submit(result):
							confirm_box.end()
							if result == 1:
								self.start_play()
						confirm_box.exe()
				else:
					Alert_Notitle(LOADPAGE_NOTEXIST_TEXT).exe()
			
			def start_play(self):
				self.end()
				play_game_from_save(saves.load(self.save_name))
			def set_save_name(self, save_name):
				self._save_name = save_name
				if saves.test_save_exists(save_name):
					self.save_data = saves.load(self.save_name)
				else:
					self.save_data = {}
			save_name = property(lambda self:self._save_name,set_save_name)
			def set_version(self, version):
				self._version = version
				self.checksum.text = version.checksum_to_str()
				self.version_box.text = version.name_to_str()
			version = property(lambda self:self._version,set_version)
			def set_save_data(self, data):
				self.version = data.get('game_version',GameVersion())
			save_data = property(lambda self:self._save_data,set_save_data)
		class GamePageMenu(MessageInteractor, UIControl):
			def __init__(self, gamepage):
				super().__init__((window,Posattr(*GAME_MENU_POS)), back = Sprite(normal_menu_back))
				
				title = Normal_Title(GAME_MENU_TITLE, GAME_MENU_TITLE_POS)
				self.title = title
				self.sons.append(title)
				
				buttons = Grid((window,Posattr(*GAME_MENU_BUTTONS_POS)), Grid_defaultlayout_gen(PADDING = 0))
				self.buttons = buttons
				self.sons.append(buttons)
				
				back_button = Normal_Button(GAME_MENU_BACK_TEXT)
				save_button = Normal_Button(GAME_MENU_SAVE_TEXT)
				achievement_button = Normal_Button(GAME_MENU_ACHIEVEMENT_TEXT)
				appendice_button = Normal_Button(GAME_MENU_APPENDICE_TEXT)
				setting_button = Normal_Button(GAME_MENU_SETTING_TEXT)
				quit_button = Normal_Button(GAME_MENU_QUIT_TEXT)
				
				buttons.sons = (back_button, save_button, achievement_button, appendice_button, setting_button, quit_button)
				buttons.relayout()
				
				@save_button.event
				def on_press():
					remove_sons(self)
					GamePageSave(gamepage).exe()
				@achievement_button.event
				def on_press():
					remove_sons(self)
					AchievementPage().exe()
				@appendice_button.event
				def on_press():
					remove_sons(self)
					AppendicePage().exe()
				@setting_button.event
				def on_press():
					remove_sons(self)
					SettingMenu().exe()
				@quit_button.event
				def on_press():
					remove_sons(self)
					confirm = ConfirmBox(GAME_CONFIRM_QUIT_TEXT)
					@confirm.event
					def on_submit(result):
						confirm.end()
						if result == 1:
							gamepage.end()
					confirm.exe()
				
				self.submit_key = (back_button, 'on_press')
				@self.event
				def on_submit():
					self.end()
					
		class GamePage(Frame,UIControl):
			def __init__(self, gamedata, load_from_save = False):
				super().__init__([window])
				gameplay = game.GamePlay(gamedata, load_from_save)
				self.gameplay = gameplay
				gamepage = self
				
				class GamePageHeader(ImageFrame):
					def __init__(self):
						super().__init__((window,Posattr(*GAME_HEADER_POS)), back = Sprite(game_header_back))
						gamepageheader = self
						
						class HeaderSwitchButton(SwitchButton):
							def __init__(self, pos = DEFAULT_POS):
								super().__init__((window,Posattr(*pos)), icons = [Sprite(game_header_switch_up_icon), Sprite(game_header_switch_down_icon)],disabled_images = [Sprite(game_header_switch_disabled_image)])
						
						messages_switch = HeaderSwitchButton(GAME_HEADER_MESSAGES_SWITCH_POS)
						character_switch = HeaderSwitchButton(GAME_HEADER_CHARACTER_SWITCH_POS)
						self.sons += (messages_switch, character_switch)
						self.messages_switch = messages_switch
						self.character_switch = character_switch
						
						class SpeedBar(Frame):
							def __init__(self):
								super().__init__((window,Posattr(*GAME_HEADER_SPEEDBAR_POS)))
								speedbar = self
								
								slider = ButtonSlider([window],layouter = ButtonSlider_defaultlayout_gen(PADDING_RATE = 0, HPADDING_RATE = 0, VPADDING_RATE = 0)) # ,back = Sprite(game_header_speedbar_back))
								self.slider = slider
								self.sons.append(slider)
								class SliderButton(SwitchButton):
									def __init__(self):
										super(SliderButton,self).__init__([window],images = [Sprite(game_header_speedbar_button_back),Sprite(game_header_speedbar_pressed_back)])
								slider.buttons = [
								SliderButton()
								for i in range(GAME_HEADER_SPEEDBAR_COUNT)]
								slider.val = 0
								@slider.event
								def on_change(val):
									gamepage.set_speed(val)
								
								label = Label((window,Middle_Posattr()),pyglet.text.Label('',font_name = GAME_HEADER_SPEEDBAR_FONT,font_size = GAME_HEADER_SPEEDBAR_FONT_SIZE,color = GAME_HEADER_SPEEDBAR_FONT_COLOR, anchor_x = 'center',anchor_y = 'center'))
								self.label = label
								self.sons.append(label)
							def refresh(self):
								self.slider._set_val(gameplay.speed)
								self.label.text = (GAME_HEADER_SPEEDBAR_PAUSE_TEXT if gameplay.speed == 0 else '') + gameplay.ui_data.time.strftime(GAME_HEADER_SPEEDBAR_TIME_FORMAT)
						speedbar = SpeedBar()
						self.speedbar = speedbar
						self.sons.append(speedbar)
						
						class SwitchPageButtons(SelectButtons):
							def __init__(self):
								super().__init__((window,Posattr(*GAME_HEADER_SWITCH_PAGE_POS)),layouter = Grid_ratelayout_gen(COLUMNS = 4, ROWS = 1, PADDING = 0, ITEM_BLANKING = 0))
								switch_page_buttons = self
								
								class SwitchPageButton(SwitchButton):
									def __init__(self, icon_image, disabled_image = None):
										icon = Sprite(icon_image)
										selected_image = Sprite(game_header_switchpage_button_select_back)
										if disabled_image is not None:
											disabled_image = Sprite(disabled_image)
										super().__init__([window], icons = [icon,icon], images = [None,selected_image], disabled_images = None if disabled_image is None else [disabled_image,disabled_image], direction = 4)
										
								self.buttons = [SwitchPageButton(game_header_switchpage_icons[i], game_header_switchpage_disabled_icons[i]) for i in range(GAME_HEADER_STATUS_SWITCHPAGE_COUNT)]
								@self.event
								def on_switch(id):
									gamepage.pages.page = id
						switch_page_buttons = SwitchPageButtons()
						self.switch_page_buttons = switch_page_buttons
						self.sons.append(switch_page_buttons)
						
						class StatusProgressBar(ProgressBar):
							def __init__(self, color = (255,255,255), pos = DEFAULT_POS, label_text = None):
								_bar = Sprite(normal_progress_bar_front)
								_bar.color = color
								_back = Sprite(normal_progress_bar_back)
								_label = None
								if label_text is not None:
									_label = Normal_ValueLabel(label_text)
								super().__init__((window,Posattr(*pos)),label = _label,back = _back,bar = _bar)
								
						class StatusIconBars(Grid):
							def __init__(self, pos):
								super().__init__((window, Posattr(*pos)),layouter = Grid_ratelayout_gen(COLUMNS = 4,ROWS = 1,PADDING = 0,ITEM_BLANKING = 0))
								class StatusIconBar(StatusProgressBar):
									def __init__(self, icon_image, color):
										icon = Sprite(icon_image)
										self.icon = icon
										super().__init__(color)
									def on_resize(self):
										super().on_resize()
										self.resize_image_direction(self.icon, 4)
									def draw(self, range = None):
										# print('drawn a button')
										super().draw(range)
										if self.icon is not None:
											self.icon.draw()
					
								self.sons = [StatusIconBar(game_header_status_bar_icons[i], GAME_HEADER_STATUS_BAR_COLORS[i]) for i in range(GAME_HEADER_STATUS_BAR_COUNT)]
								self.relayout()
								
						status_bars = StatusIconBars(GAME_HEADER_STATUS_BARS_POS)
						self.status_bars = status_bars
						self.sons.append(status_bars)
							
						rating_bar = StatusProgressBar(GAME_HEADER_RATING_BAR_DEFAULT_COLOR, GAME_HEADER_RATING_BAR_POS, '')
						self.rating_bar = rating_bar
						self.sons.append(rating_bar)
						
						menu_button = Normal_Button(GAME_HEADER_MENU_BUTTON_TEXT,GAME_HEADER_MENU_BUTTON_POS)
						self.sons.append(menu_button)
						
						@messages_switch.event
						def on_press():
							messages_switch.stage ^= 1
						@character_switch.event
						def on_press():
							character_switch.stage ^= 1
						@menu_button.event
						def on_press():
							gameplay.pause()
							GamePageMenu(gamepage).exe()
				
				header = GamePageHeader()
				self.header = header
				self.sons.append(header)
				
				class GamePage_StrategyPlanBox(ScrollFrame):
					# 载入、显示及浏览存档
					def __init__(self,  pos = DEFAULT_POS):
						super().__init__((window, Posattr(*pos)))
						
						select_list_buttons = SelectButtons([window],layouter = Grid_defaultlayout_gen(ITEM_HEIGHT = GAME_SLPLAN_SELECT_ITEM_HEIGHT, ITEM_BLANKING = GAME_SLPLAN_SELECT_ITEM_BLANKING, PADDING = 0), canceling = True)
						self.frame = select_list_buttons
						
						scrollbar = Normal_ScrollBar()
						self.scrollbar = scrollbar
						
						@select_list_buttons.event
						def on_switch(button):
							if button < 0 or button >= len(select_list_buttons.buttons):
								self.dispatch_event('on_select_plan', None)
							else:
								self.dispatch_event('on_select_plan', select_list_buttons.buttons[button].key)
					def refresh(self):
						self.frame.buttons = gameplay.ui_data.select_strategy_plans
						if self.visible:
							self.show()
						self.scrollbar.rate = 0
						self.frame.button = -1
						self.on_resize()
				GamePage_StrategyPlanBox.register_event_type('on_select_plan')
				
				class GamePage_SLStrategyPlan(MessageInteractor, UIControl):
					def __init__(self):
						super().__init__((window,Posattr(*GAME_SLPLAN_POS)), back = Sprite(normal_menu_back))
						
						title = Normal_Title(GAME_SLPLAN_TITLE, GAME_SLPLAN_TITLE_POS)
						self.title = title
						self.sons.append(title)
						
						info = Normal_ScrollText('', GAME_SLPLAN_INFO_POS)
						self.info = info
						self.sons.append(info)
						
						select = GamePage_StrategyPlanBox(GAME_SLPLAN_SELECT_POS)
						self.select = select
						self.sons.append(select)
						
						class GamePages_Timetable_PlanFrame_Button(Button):
							def __init__(self, icon_image):
								super().__init__([window], image = Sprite(game_slplan_button_back), icon = Sprite(icon_image), pressed_image = Sprite(game_slplan_button_pressed_back), direction = 4)
						
						buttons_grid = Grid((window, Posattr(*GAME_SLPLAN_BUTTONS_POS)),layouter = Grid_ratelayout_gen(ROWS = 1, COLUMNS = 4, PADDING = 0, ITEM_BLANKING = 0))
						self.buttons_grid = buttons_grid
						self.sons.append(buttons_grid)
						
						copy_button = GamePages_Timetable_PlanFrame_Button(game_slplan_copy_icon)
						remove_button = GamePages_Timetable_PlanFrame_Button(game_slplan_remove_icon)
						use_button = GamePages_Timetable_PlanFrame_Button(game_slplan_use_icon)
						rename_button = GamePages_Timetable_PlanFrame_Button(game_slplan_rename_icon)
						buttons_grid.sons = [copy_button, remove_button, use_button, rename_button]
						buttons_grid.relayout()
						
						confirm_button = Button((window, Posattr(*GAME_SLPLAN_CONFIRM_POS)), image = Sprite(game_slplan_confirm_image))
						self.sons.append(confirm_button)
						self.submit_key = (confirm_button, 'on_press')
						
						self.__dict__.update({key:value for key,value in locals().items() if key[-7:] == '_button'})
					def refresh(self):
						self.select.refresh()
						
				class GamePages(MultiPage):
					def __init__(self):
						super().__init__((window, Posattr(*GAME_PAGES_POS)))
						
						class GamePages_Page(ImageFrame):
							def __init__(self, back_image):
								super().__init__([window],back = Sprite(back_image))
								
						class GamePages_Character(ImageFrame):
							def __init__(self):
								super().__init__([window], back = Sprite(game_pages_character_back))
								back_image = SpriteControl((window,Posattr(*GAME_PAGES_CHARACTER_BACK_POS)))
								self.back_image = back_image
								front_image = SpriteControl((window,Posattr(*GAME_PAGES_CHARACTER_FRONT_POS)))
								self.front_image = front_image
								
								self.sons += (back_image, front_image)
							def refresh(self):
								self.back_image.image, self.front_image.image = gameplay.ui_data.pages_character_ui
								self.on_resize()
								
						class GamePages_Timetable(ImageFrame):
							def __init__(self):
								super().__init__([window], back = Sprite(game_pages_timetable_back))
								
								class GamePages_Timetable_MessageFrame(ImageFrame):
									def __init__(self, title_text = '', pos = DEFAULT_POS):
										super().__init__((window, Posattr(*pos)), back = Sprite(game_pages_timetable_frame_back))
										
										title = Normal_Title2(title_text, GAME_PAGES_TIMETABLE_FRAME_LABEL_POS)
										self.title = title
										self.sons.append(title)
										
										left_button = Button((window,Posattr(*GAME_PAGES_TIMETABLE_FRAME_LEFT_BUTTON_POS)),image = Sprite(game_pages_timetable_frame_left_button_image))
										self.left_button = left_button
										self.sons.append(left_button)
										
										right_button = Button((window,Posattr(*GAME_PAGES_TIMETABLE_FRAME_RIGHT_BUTTON_POS)),image = Sprite(game_pages_timetable_frame_right_button_image))
										self.right_button = right_button
										self.sons.append(right_button)
										
										item_grid = Grid((window,Posattr(*GAME_PAGES_TIMETABLE_FRAME_BOARD_POS)),layouter = Grid_defaultlayout_gen(PADDING = 0,ITEM_BLANKING = 0,ITEM_HEIGHT = GAME_PAGES_TIMETABLE_MESSAGES_ITEM_HEIGHT,CAL_ABSH = False))
										self.item_grid = item_grid
										self.sons.append(item_grid)
								
								timetable = GamePages_Timetable_MessageFrame(GAME_PAGES_TIMETABLE_TIMETABLE_TEXT, GAME_PAGES_TIMETABLE_TIMETABLE_POS)
								self.timetable = timetable
								
								log = GamePages_Timetable_MessageFrame(GAME_PAGES_TIMETABLE_LOG_TEXT, GAME_PAGES_TIMETABLE_LOG_POS)
								self.log = log
								
								self.sons += (timetable, log)
								
								class GamePages_Timetable_ScrollStrategyFrame(ImageFrame):
									def __init__(self, title_text = '', pos = DEFAULT_POS):
										super().__init__((window, Posattr(*pos)), back = Sprite(game_pages_timetable_frame_back))
										
										title = Normal_Title2(title_text, GAME_PAGES_TIMETABLE_FRAME_LABEL_POS)
										self.title = title
										self.sons.append(title)
											
										item_frame = SelectButtons([window],layouter = Grid_defaultlayout_gen(PADDING = 0,ITEM_BLANKING = 0,ITEM_HEIGHT = GAME_PAGES_TIMETABLE_MESSAGES_STRATEGY_ITEM_HEIGHT), canceling = True)
										# 越级访问
										self.item_frame = item_frame
										
										scrollbar = Normal_ScrollBar()
										self.scrollbar = scrollbar
										
										scroll_frame = ScrollFrame((window,Posattr(*GAME_PAGES_TIMETABLE_FRAME_BOARD_POS)))
										self.scroll_frame = scroll_frame
										self.sons.append(scroll_frame)
										scroll_frame.frame = item_frame
										scroll_frame.scrollbar = scrollbar
										
								class GamePages_Timetable_PlanFrame(GamePages_Timetable_ScrollStrategyFrame):
									def __init__(self, title_text = '', pos = DEFAULT_POS):
										super().__init__(title_text, pos)
										self.scroll_frame.pos = Posattr(*GAME_PAGES_TIMETABLE_PLAN_BOARD_POS)
										
										buttons_grid = Grid((window, Posattr(*GAME_PAGES_TIMETABLE_PLAN_BUTTONS_POS)),layouter = Grid_ratelayout_gen(ROWS = 1, COLUMNS = 6, PADDING = 0, ITEM_BLANKING = 0))
										self.buttons_grid = buttons_grid
										self.sons.append(buttons_grid)

										class GamePages_Timetable_PlanFrame_Button(Button):
											def __init__(self, icon_image):
												super().__init__([window], image = Sprite(game_pages_timetable_frame_plan_button_back), icon = Sprite(icon_image), pressed_image = Sprite(game_pages_timetable_frame_plan_button_pressed_back), direction = 4)
										
										add_button = GamePages_Timetable_PlanFrame_Button(game_pages_timetable_plan_add_icon)
										edit_button = GamePages_Timetable_PlanFrame_Button(game_pages_timetable_plan_edit_icon)
										remove_button = GamePages_Timetable_PlanFrame_Button(game_pages_timetable_plan_remove_icon)
										save_button = GamePages_Timetable_PlanFrame_Button(game_pages_timetable_plan_save_icon)
										# load_button = GamePages_Timetable_PlanFrame_Button(game_pages_timetable_plan_load_icon)
										moveup_button = GamePages_Timetable_PlanFrame_Button(game_pages_timetable_plan_moveup_icon)
										movedown_button = GamePages_Timetable_PlanFrame_Button(game_pages_timetable_plan_movedown_icon)
										shiftup_button = GamePages_Timetable_PlanFrame_Button(game_pages_timetable_plan_shiftup_icon)
										shiftdown_button = GamePages_Timetable_PlanFrame_Button(game_pages_timetable_plan_shiftdown_icon)
										# sl_grid = UDButtons([window],[save_button,load_button])
										move_grid = LRButtons([window],[moveup_button,movedown_button])
										shift_grid = UDButtons([window],[shiftup_button,shiftdown_button])
																											
										self.__dict__.update({key:value for key,value in locals().items() if key[-7:] == '_button'})
										buttons_grid.sons = (add_button, edit_button, remove_button, save_button, move_grid, shift_grid)
										buttons_grid.relayout()

										strategy_cursor = SpriteControl([window], image = Sprite(game_message_strategy_cursor), fixed_ratio = False)
										strategy_cursor.opacity = True
										self.strategy_cursor = strategy_cursor
										self.sons.append(strategy_cursor)
										
										@save_button.event
										def on_press():
											GamePage_SLStrategyPlan().exe()
										
								plan = GamePages_Timetable_PlanFrame(GAME_PAGES_TIMETABLE_PLAN_TEXT, GAME_PAGES_TIMETABLE_PLAN_POS)
								self.plan = plan
								self.sons.append(plan)
								
								strategy = GamePages_Timetable_ScrollStrategyFrame(GAME_PAGES_TIMETABLE_STRATEGY_TEXT, GAME_PAGES_TIMETABLE_STRATEGY_POS)
								self.strategy = strategy
								self.sons.append(strategy)
							def refresh(self):
								pass
								
						class GamePages_Ability(ImageFrame):
							def __init__(self):
								super().__init__([window], back = Sprite(game_pages_ability_back))
							def refresh(self):
								pass
								
						class GamePages_Contest(ImageFrame):
							def __init__(self):
								super().__init__([window], back = Sprite(game_pages_contest_back))
							def refresh(self):
								pass
								
						character_page = GamePages_Character()
						self.character_page = character_page
						
						timetable_page = GamePages_Timetable()
						self.timetable_page = timetable_page
						
						ability_page = GamePages_Ability()
						self.ability_page = ability_page
						
						contest_page = GamePages_Contest()
						self.contest_page = contest_page
						
						self.pages = (character_page, timetable_page, ability_page, contest_page)	
				
				pages = GamePages()
				self.pages = pages
				self.sons.append(pages)
				
				class GameMessagesBoard(ImageFrame):
					def __init__(self):
						super().__init__((window,Posattr(*GAME_MESSAGES_BOARD_POS)), back = Sprite(game_board_back))
						
						timetable_label = Normal_Label(GAME_MESSAGES_BOARD_TIMETABLE_TEXT,GAME_MESSAGES_BOARD_TIMETABLE_LABEL_POS,anchor_x = 'center')
						self.timetable_label = timetable_label
						self.sons.append(timetable_label)
						
						timetable = Grid((window,Posattr(*GAME_MESSAGES_BOARD_TIMETABLE_POS)),layouter = Grid_defaultlayout_gen(PADDING = 0,ITEM_BLANKING = 0,ITEM_HEIGHT = GAME_MESSAGES_BOARD_TIMETABLE_ITEM_HEIGHT,CAL_ABSH = False))
						self.timetable = timetable
						self.sons.append(timetable)
						
						log_label = Normal_Label(GAME_MESSAGES_BOARD_LOG_TEXT,GAME_MESSAGES_BOARD_LOG_LABEL_POS,anchor_x = 'center')
						self.log_label = log_label
						self.sons.append(log_label)
						
						log = Grid((window,Posattr(*GAME_MESSAGES_BOARD_LOG_POS)),layouter = Grid_defaultlayout_gen(PADDING = 0,ITEM_BLANKING = 0,ITEM_HEIGHT = GAME_MESSAGES_BOARD_LOG_ITEM_HEIGHT,CAL_ABSH = False))
						self.log = log
						self.sons.append(log)
						
						plan_label = Normal_Label(GAME_MESSAGES_BOARD_PLAN_TEXT,GAME_MESSAGES_BOARD_PLAN_LABEL_POS,anchor_x = 'center')
						self.plan_label = plan_label
						self.sons.append(plan_label)
						
						plan = Grid((window,Posattr(*GAME_MESSAGES_BOARD_PLAN_POS)),layouter = Grid_defaultlayout_gen(PADDING = 0,ITEM_BLANKING = 0,ITEM_HEIGHT = GAME_MESSAGES_BOARD_PLAN_ITEM_HEIGHT,CAL_ABSH = False))
						self.plan = plan
						self.sons.append(plan)
						
						strategy_label = Normal_Label(GAME_MESSAGES_BOARD_STRATEGY_TEXT,GAME_MESSAGES_BOARD_STRATEGY_LABEL_POS,anchor_x = 'center')
						self.strategy_label = strategy_label
						self.sons.append(strategy_label)
						
						strategy_buttons = SelectButtons([window],layouter = Grid_defaultlayout_gen(PADDING = 0,ITEM_BLANKING = 0,ITEM_HEIGHT = GAME_MESSAGES_BOARD_STRATEGY_ITEM_HEIGHT), canceling = True)
						# 越级访问
						self.strategy_buttons = strategy_buttons
						
						strategy_scroll = Normal_ScrollBar()
						self.strategy_scroll = strategy_scroll
						
						strategy_frame = ScrollFrame((window,Posattr(*GAME_MESSAGES_BOARD_STRATEGY_POS)))
						self.strategy_frame = strategy_frame
						self.sons.append(strategy_frame)
						strategy_frame.frame = strategy_buttons
						strategy_frame.scrollbar = strategy_scroll
						
						strategy_cursor = SpriteControl([window], image = Sprite(game_message_strategy_cursor), fixed_ratio = False)
						strategy_cursor.opacity = True
						self.strategy_cursor = strategy_cursor
						self.sons.append(strategy_cursor)
						
						@strategy_buttons.event
						def on_switch(button):
							if button == -1:
								gameplay.current_strategy = None
							else:
								gameplay.current_strategy = strategy_buttons.buttons[button].key
					def on_resize(self):
						super().on_resize()
						if hasattr(self, 'plan'):
							if self.plan.sons:
								self.strategy_cursor.abspos = self.plan.sons[0].abspos
					def show(self):
						super().show()
						if hasattr(self, 'plan'):
							if self.plan.sons:
								self.strategy_cursor.show()
							else:
								self.strategy_cursor.hide()
					def refresh(self):
						self.timetable.sons, self.log.sons, self.plan.sons, strategy_items = gameplay.ui_data.messages_board_ui
						self.strategy_buttons._set_buttons(strategy_items)
						self.strategy_buttons._set_button(-1)
						for i in range(len(strategy_items)):
							if gameplay.current_strategy == strategy_items[i].key:
								self.strategy_buttons._set_button(i)
								break
						for i in self.plan.sons:
							@i.event
							def on_press():
								self.strategy_buttons.button = -1
						for i in self.plan.sons:
							i.stage = 0
						if self.plan.sons and gameplay.current_strategy is None:
							self.plan.sons[0].stage = 1
						self.timetable.relayout()
						self.log.relayout()
						self.plan.relayout()
						self.strategy_buttons.relayout()
						self.on_resize()
						if self.visible:
							self.show()
						
				class GameCharacterBoard(ImageFrame):
					def __init__(self):
						super().__init__((window,Posattr(*GAME_CHARACTER_BOARD_POS)), back = Sprite(game_board_back))
						image = SpriteControl((window,Posattr(*GAME_CHARACTER_BOARD_IMAGE_POS)))
						self.image = image
						self.sons.append(image)
						
						title = Normal_Title('',GAME_CHARACTER_BOARD_TITLE_POS)
						self.title = title
						self.sons.append(title)
						
						info = Grid((window,Posattr(*GAME_CHARACTER_BOARD_INFO_POS)),layouter = Grid_defaultlayout_gen(COLUMNS = 1,PADDING = 0,ITEM_BLANKING = 0,ITEM_HEIGHT = None))
						info.sons = [Normal_Label('', anchor_x = 'center') for i in range(GAME_CHARACTER_BOARD_INFO_COUNT)]
						self.info = info
						self.sons.append(info)
					def refresh(self):
						self.image.image ,self.title.text ,infotexts = gameplay.ui_data.character_board_ui
						for i in range(GAME_CHARACTER_BOARD_INFO_COUNT):
							self.info.sons[i].text = infotexts[i]
						self.info.relayout()
						self.on_resize()
						if self.visible:
							self.show()
				
				messages_board = GameMessagesBoard()
				character_board = GameCharacterBoard()
				self.messages_board = messages_board
				self.character_board = character_board
				self.sons += (messages_board, character_board)
				
				@pages.event				
				def on_switch(page):
					if page == 1:
						header.messages_switch.stage = 0
						header.messages_switch.disabled = True
					else:
						header.messages_switch.disabled = False
					pages.pages[page].refresh()
				@header.messages_switch.event
				def on_switch(stage):
					if stage:
						messages_board.show()
					else:
						messages_board.hide()
				@header.character_switch.event
				def on_switch(stage):
					if stage:
						character_board.show()
					else:
						character_board.hide()
						
				header.messages_switch.stage = 1
				header.character_switch.stage = 1
				
				@gameplay.event
				def on_update_speed_time():
					self.refresh_speed_time()
				@gameplay.event
				def on_update_message():
					self.refresh_message_board()
				@gameplay.event
				def on_update_pages_character():
					self.refresh_pages_character()
				@gameplay.event
				def on_update():
					self.refresh()
			def set_speed(self, v):
				self.gameplay.speed = v
			def refresh_speed_time(self):
				self.header.speedbar.refresh()
			def refresh_character_board(self):
				self.character_board.refresh()
			def refresh_message_board(self):
				self.messages_board.refresh()
			def refresh_pages_character(self):
				self.pages.character_page.refresh()
			def refresh(self):
				self.refresh_speed_time()
				self.refresh_character_board()
				self.refresh_message_board()
				self.refresh_pages_character()
				# 刷新UI
			def exe(self):
				# 使用类名调用父类函数 -- 注意
				self.gameplay._play()
				UIControl.exe(self)
			def end(self):
				UIControl.end(self)
				self.gameplay._end()
		def play_game_from_scenario(scenario):
			gamedata = data.get(['GAME_DEFINE',scenario.game_define])
			gamedata['scenario'] = scenario.key
			GamePage(gamedata,False).exe()
		def play_game_from_save(save_data):
			GamePage(save_data,True).exe()
		@window.event
		def on_resize(width, height):
			root.width = width
			root.height = height
			root.on_resize()
		
		@window.event
		def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
		# 覆盖系统事件，不加这个会很卡
			pass
		
		MainMenu().exe()
		
		if data.get(['_DEBUG'], False):
			# FPS(DEBUG)
			fps_display = pyglet.clock.ClockDisplay()
			def window_on_draw():
				window.clear()
				root.draw()
				fps_display.draw()
			window.on_draw = window_on_draw
		
		self.__dict__.update({key:value for key,value in locals().items() if key != 'self'})
		
ui = UI()