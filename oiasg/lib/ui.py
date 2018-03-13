#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
import pyglet

from .controls import *
from .game import *
from .data import *

class UI(pyglet.event.EventDispatcher):
	def init_settings(self):
		self.fullscreen = self.data.get(['FULLSCREEN'])
		self.volume_music = self.data.get(['VOLUME_MUSIC'])
		self.volume_effect = self.data.get(['VOLUME_EFFECT'])
		self.volume_game = self.data.get(['VOLUME_GAME'])
	def reset_settings(self):
		self.fullscreen = self.data.get(['FULLSCREEN_DEFAULT'])
		self.volume_music = self.data.get(['VOLUME_MUSIC_DEFAULT'])
		self.volume_effect = self.data.get(['VOLUME_EFFECT_DEFAULT'])
		self.volume_game = self.data.get(['VOLUME_GAME_DEFAULT'])
	def __init__(self,gameobj):
		data = gameobj.data
		resource = gameobj.resource
		saves = gameobj.saves
		self.data = data
		self.resource = resource
		self.saves = saves
		
		ui = self
		
		globals().update(data.get_all_dict(['UI'])) # 引入命名空间
		
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
	
		# 预加载资源
		
		normal_button_back = resource.load_image(NORMAL_BUTTON_BACK)
		normal_button_pressed_back = resource.load_image(NORMAL_BUTTON_PRESSED_BACK)
		normal_menu_back = resource.load_image(NORMAL_MENU_BACK)
		normal_page_back = resource.load_image(NORMAL_PAGE_BACK)
		normal_default_image = resource.load_image(NORMAL_DEFAULT_IMAGE)
		normal_slider_back = resource.load_image(NORMAL_SLIDER_BACK)
		normal_slider_cursor = resource.load_image(NORMAL_SLIDER_CURSOR)
		normal_checkbox_unchecked_back = resource.load_image(NORMAL_CHECKBOX_UNCHECKED_BACK)
		normal_checkbox_checked_back = resource.load_image(NORMAL_CHECKBOX_CHECKED_BACK)
		normal_scrollbar_back = resource.load_image(NORMAL_SCROLLBAR_BACK)
		normal_scrollbar_cursor = resource.load_image(NORMAL_SCROLLBAR_CURSOR)
		normal_switchbutton_back = resource.load_image(NORMAL_SWITCHBUTTON_BACK)
		normal_switchbutton_select_back = resource.load_image(NORMAL_SWITCHBUTTON_SELECT_BACK)
		normal_tag_rv_back = resource.load_image(NORMAL_TAG_RV_IMAGE)
		normal_tag_rv_selected_back = resource.load_image(NORMAL_TAG_RV_SELECTED_IMAGE)
		normal_progress_bar_front = resource.load_image(NORMAL_PROGRESS_BAR_FRONT)
		normal_progress_bar_back = resource.load_image(NORMAL_PROGRESS_BAR_BACK)
		
		main_menu_back = resource.load_image(MAIN_MENU_BACK)
		main_menu_start_back = resource.load_image(MAIN_MENU_START_BACK)
		main_menu_start_pressed_back = resource.load_image(MAIN_MENU_START_PRESSED_BACK)
		
		game_page_header_back = resource.load_image(GAME_PAGE_HEADER_BACK)
		game_page_header_speedbar_back = resource.load_image(GAME_PAGE_HEADER_SPEEDBAR_BACK)
		game_page_header_speedbar_button_back = resource.load_image(GAME_PAGE_HEADER_SPEEDBAR_BUTTON_BACK)
		game_page_header_speedbar_pressed_back = resource.load_image(GAME_PAGE_HEADER_SPEEDBAR_BUTTON_PRESSED_BACK)
		
		game_pages_character_back = resource.load_image(GAME_PAGES_CHARACTER_BACK)
		game_pages_timetable_back = resource.load_image(GAME_PAGES_TIMETABLE_BACK)
		game_pages_ability_back = resource.load_image(GAME_PAGES_ABILITY_BACK)
		game_pages_contest_back = resource.load_image(GAME_PAGES_CONTEST_BACK)
		
		game_header_bar_health_icon = resource.load_image(GAME_HEADER_BAR_HEALTH_ICON)
		game_header_bar_mood_icon = resource.load_image(GAME_HEADER_BAR_MOOD_ICON)
		game_header_bar_stress_icon = resource.load_image(GAME_HEADER_BAR_STRESS_ICON)
		game_header_bar_ability_icon = resource.load_image(GAME_HEADER_BAR_ABILITY_ICON)
		
		game_header_character_icon = resource.load_image(GAME_HEADER_CHARACTER_ICON)
		game_header_timetable_icon = resource.load_image(GAME_HEADER_TIMETABLE_ICON)
		game_header_ability_icon = resource.load_image(GAME_HEADER_ABILITY_ICON)
		game_header_contest_icon = resource.load_image(GAME_HEADER_CONTEST_ICON)
		game_header_contest_disabled_icon = resource.load_image(GAME_HEADER_CONTEST_DISABLED_ICON)
		game_header_switchpage_button_select_back = resource.load_image(GAME_HEADER_SWITCHPAGE_BUTTON_SELECT_BACK)
		
		class Middle_Posattr(Posattr):
			def __init__(self):
				super(Middle_Posattr,self).__init__((0.5,0),(0.5,0),(0,0),(0,0))
		class Normal_ButtonLabel(pyglet.text.Label):
			def __init__(self, text):
				super(Normal_ButtonLabel,self).__init__(text,font_name = NORMAL_BUTTON_FONT,font_size = NORMAL_BUTTON_FONT_SIZE,color = NORMAL_BUTTON_FONT_COLOR,anchor_x = 'center',anchor_y = 'center')
		class Normal_ValueLabel(pyglet.text.Label):
			def __init__(self, text):
				super(Normal_ValueLabel,self).__init__(text,font_name = NORMAL_VALUE_FONT,font_size = NORMAL_VALUE_FONT_SIZE,color = NORMAL_VALUE_FONT_COLOR,anchor_x = 'center',anchor_y = 'center')
		class Normal_Title0(Label):
			def __init__(self, parent,text,pos = DEFAULT_POS):
				super(Normal_Title0,self).__init__((window,parent,Posattr(*pos)),pyglet.text.Label(text,font_name = NORMAL_TITLE0_FONT,font_size = NORMAL_TITLE0_FONT_SIZE,color = NORMAL_TITLE0_COLOR, anchor_x = 'center',anchor_y = 'center'))
		class Normal_Title(Label):
			def __init__(self, parent,text,pos = DEFAULT_POS):
				super(Normal_Title,self).__init__((window,parent,Posattr(*pos)),pyglet.text.Label(text,font_name = NORMAL_TITLE_FONT,font_size = NORMAL_TITLE_FONT_SIZE,color = NORMAL_TITLE_COLOR, anchor_x = 'center',anchor_y = 'center'))
		class Normal_Title2(Label):
			def __init__(self, parent,text,pos = DEFAULT_POS):
				super(Normal_Title2,self).__init__((window,parent,Posattr(*pos)),pyglet.text.Label(text,font_name = NORMAL_TITLE2_FONT,font_size = NORMAL_TITLE2_FONT_SIZE,color = NORMAL_TITLE2_COLOR, anchor_x = 'center',anchor_y = 'center'))
		class Normal_Label(Label):
			def __init__(self, parent,text,pos = DEFAULT_POS):
				super(Normal_Label,self).__init__((window,parent,Posattr(*pos)),pyglet.text.Label(text,font_name = NORMAL_LABEL_FONT,font_size = NORMAL_LABEL_FONT_SIZE,color = NORMAL_LABEL_COLOR, anchor_x = 'left',anchor_y = 'center'))
		class Normal_MessageText(TextBox):
			def __init__(self,parent,text,pos = DEFAULT_POS):
				super(Normal_MessageText,self).__init__((window,parent,Posattr(*pos)),text,NORMAL_MESSAGE_TEXT_STYLE,multiline = True)
		class Normal_TextInput(TextBox):
			def __init__(self, parent, text, pos = DEFAULT_POS):
				super(Normal_TextInput,self).__init__((window, parent, Posattr(*pos)),text,NORMAL_INPUT_TEXT_STYLE,editable = True,multiline = False,select_backcolor = NORMAL_INPUT_TEXT_SELECT_BACKCOLOR, select_textcolor = NORMAL_INPUT_TEXT_SELECT_TEXTCOLOR, caret_color = NORMAL_INPUT_TEXT_SELECT_CARETCOLOR)
		class Normal_Button(Button):
			def __init__(self, parent,labeltext,pos = DEFAULT_POS):
				super(Normal_Button,self).__init__(
					(window,parent,Posattr(*pos)),
					label = Normal_ButtonLabel(labeltext),
					image = Sprite(normal_button_back),
					pressed_image = Sprite(normal_button_pressed_back),
					hover_color = NORMAL_BUTTON_HOVER_COLOR,
					color = NORMAL_BUTTON_COLOR
				)
		class Normal_Slider(Slider):
			def __init__(self, parent,pos = DEFAULT_POS):
				super(Normal_Slider, self).__init__(
					(window,parent,Posattr(*pos)),
					image = Sprite(normal_slider_back),
					cursor = Sprite(normal_slider_cursor)
				)
		class Normal_Checkbox(SwitchButton):
			def __init__(self, parent,pos = DEFAULT_POS):
				super(Normal_Checkbox,self).__init__(
					(window,parent,Posattr(*pos)),
					images = (
						Sprite(normal_checkbox_unchecked_back),
						Sprite(normal_checkbox_checked_back)
					),
					hover_color = NORMAL_BUTTON_HOVER_COLOR,
					color = NORMAL_BUTTON_COLOR
				)
		class Normal_FormattedText(FormattedTextBox):
			def __init__(self, parent,text,pos = DEFAULT_POS):
				super(Normal_FormattedText, self).__init__((window,parent,Posattr(*pos)),resource.decode_text(text),multiline = True)
		class Normal_ScrollBar(ScrollBar):
			def __init__(self, parent,pos = DEFAULT_POS):
				super(Normal_ScrollBar,self).__init__((window,parent,Posattr(*pos)), image = Sprite(normal_scrollbar_back), cursor = Sprite(normal_scrollbar_cursor))
		class Normal_SwitchButton(SwitchButton):
			def __init__(self,parent,text,pos = DEFAULT_POS):
				title = Normal_ButtonLabel(text)
				super(Normal_SwitchButton,self).__init__(
					(window,parent,pos),
					[title,title],
					[Sprite(normal_switchbutton_back),Sprite(normal_switchbutton_select_back)],
					hover_color = NORMAL_BUTTON_HOVER_COLOR,
					color = NORMAL_BUTTON_COLOR
				)
		class Normal_Tag_rv(SwitchButton):
			def __init__(self, parent,text,pos = DEFAULT_POS):
				title = Normal_ButtonLabel(text)
				super(Normal_Tag_rv,self).__init__(
					(window,parent,pos),
					[title,title],
					[Sprite(normal_tag_rv_back),Sprite(normal_tag_rv_selected_back)],
					hover_color = NORMAL_BUTTON_HOVER_COLOR,
					color = NORMAL_BUTTON_COLOR
				)
		class Normal_ScrollText(ScrollTextBox):
			def __init__(self,parent,text,pos = DEFAULT_POS):
				super(Normal_ScrollText,self).__init__((window,parent,Posattr(*pos)))
				doc = Normal_MessageText(self,text)
				scrollbar = Normal_ScrollBar(self)
				self.doc = doc
				self.scrollbar = scrollbar
		class Normal_ScrollFormattedText(ScrollTextBox):
			def __init__(self,parent,text,pos = DEFAULT_POS):
				super(Normal_ScrollFormattedText,self).__init__((window,parent,Posattr(*pos)))
				doc = Normal_FormattedText(self,text)
				scrollbar = Normal_ScrollBar(self)
				self.doc = doc
				self.scrollbar = scrollbar
						
		# 对 UI 特化的控件类，用于UI中的独立界面
		# 不符合替换原则
		class UIControl(object):
			def exe(self):
				# 执行该控件
				push_control(self)
			def end(self):
				remove_control(self)
			def refresh(self):
				# 刷新数据
				pass
		class Alert(AlertBox,UIControl):
			def __init__(self, text, title, pos = NORMAL_ALERT_POS):
				super(Alert,self).__init__((window,root,Posattr(*pos)),back = Sprite(normal_menu_back),layouter = AlertBox_defaultlayout_gen())
				alert_text = Normal_MessageText(self,text)
				self.doc = alert_text
				alert_title = Normal_Title(self,title)
				self.title = alert_title
				alert_button = Normal_Button(self,NORMAL_ALERT_BUTTON_TEXT)
				self.button = alert_button
				@self.event
				def on_submit():
					self.end()
		class Alert_Notitle(AlertBox,UIControl):
			def __init__(self, text, pos = NORMAL_ALERT_NOTITLE_POS):
				super(Alert_Notitle,self).__init__((window,root,Posattr(*pos)),back = Sprite(normal_menu_back),layouter = AlertBox_defaultlayout_gen(TITLE_HEIGHT = 0))
				alert_text = Normal_MessageText(self,text)
				self.doc = alert_text
				alert_button = Normal_Button(self,NORMAL_ALERT_BUTTON_TEXT)
				self.button = alert_button
				@self.event
				def on_submit():
					self.end()
		class MediaPage(MediaPlayer,UIControl):
			def __init__(self, media, loop = False):
				super(MediaPage,self).__init__((window,root))
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
		# 设置菜单
		class SettingMenu(MessageInteractor,UIControl):
			def __init__(self):
				super(SettingMenu,self).__init__((window,root,Posattr(*SETTING_MENU_POS)),back = Sprite(normal_menu_back))
				
				title = Normal_Title(self,SETTING_MENU_TITLE, SETTING_MENU_TITLE_POS)
				self.sons.append(title)
				self.title = title
				
				confirm = Normal_Button(self,SETTING_MENU_CONFIRM_TEXT,SETTING_MENU_CONFIRM_POS)
				self.sons.append(confirm)
				self.confirm = confirm
				self.submit_key = (confirm,'on_press')
				
				reset = Normal_Button(self,SETTING_MENU_RESET_TEXT,SETTING_MENU_RESET_POS)
				@reset.event
				def on_press():
					ui.reset_settings()
					self.refresh()
				self.sons.append(reset)
				self.reset = reset
				
				sound = Frame((window,self,Posattr(*SETTING_MENU_SOUND_FRAME_POS)))
				self.sons.append(sound)
				self.sound = sound
				
				sound_label = Normal_Title2(sound, SETTING_MENU_SOUND_TITLE, SETTING_MENU_SOUND_TITLE_POS)
				sound.sons.append(sound_label)
				self.sound_label = sound_label
				
				volume_music = Normal_Slider(sound, SETTING_MENU_VOLUME_MUSIC_POS)
				volume_music_label = Normal_Label(sound, SETTING_MENU_VOLUME_MUSIC_TEXT, SETTING_MENU_VOLUME_MUSIC_LABEL_POS)
				@volume_music.event
				def on_change(val):
					ui.volume_music = val
				sound.sons += (volume_music,volume_music_label)
				self.volume_music = volume_music
				self.volume_music_label = volume_music_label
				
				volume_effect = Normal_Slider(sound, SETTING_MENU_VOLUME_EFFECT_POS)
				volume_effect_label = Normal_Label(sound, SETTING_MENU_VOLUME_EFFECT_TEXT, SETTING_MENU_VOLUME_EFFECT_LABEL_POS)
				@volume_effect.event
				def on_change(val):
					ui.volume_effect = val
				sound.sons += (volume_effect,volume_effect_label)
				self.volume_effect = volume_effect
				self.volume_effect_label = volume_effect_label
				
				volume_game = Normal_Slider(sound, SETTING_MENU_VOLUME_GAME_POS)
				volume_game_label = Normal_Label(sound, SETTING_MENU_VOLUME_GAME_TEXT, SETTING_MENU_VOLUME_GAME_LABEL_POS)
				@volume_game.event
				def on_change(val):
					ui.volume_game = val
				sound.sons += (volume_game,volume_game_label)
				self.volume_game = volume_game
				self.volume_game_label = volume_game_label
				
				fullscreen = Normal_Checkbox(self,SETTING_MENU_FULLSCREEN_POS)
				fullscreen_label = Normal_Label(self, SETTING_MENU_FULLSCREEN_TEXT, SETTING_MENU_FULLSCREEN_LABEL_POS)
				@fullscreen.event
				def on_press():
					fullscreen.stage ^= 1
				@fullscreen.event
				def on_switch(val):
					ui.fullscreen = bool(val)
				self.sons += (fullscreen, fullscreen_label)
				self.fullscreen = fullscreen
				self.fullscreen_label = fullscreen_label
				
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
				super(ConfirmBox,self).__init__((window,root,Posattr(*pos)),back = Sprite(normal_menu_back),layouter = MessageBox_defaultlayout_gen(TITLE_HEIGHT = 0))
				
				text = Normal_MessageText(self,text)
				self.doc = text
				yes = Normal_Button(self,CONFIRM_BOX_YES_TEXT)
				no = Normal_Button(self,CONFIRM_BOX_NO_TEXT)
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
				super(VersionPage,self).__init__((window,root,Posattr(*VERSION_PAGE_POS)),back = Sprite(normal_menu_back),layouter = AlertBox_defaultlayout_gen())
				alert_text = Normal_ScrollText(self,text)
				self.doc = alert_text
				alert_title = Normal_Title(self,VERSION_PAGE_TITLE)
				self.title = alert_title
				alert_button = Normal_Button(self,NORMAL_ALERT_BUTTON_TEXT)
				self.button = alert_button
				@self.event
				def on_submit():
					self.end()
		# 关于页面
		class AboutPage(AlertBox,UIControl):
			def __init__(self):
				super(AboutPage,self).__init__((window,root,Posattr(*ABOUT_PAGE_POS)),
				back = Sprite(normal_menu_back),layouter = AlertBox_defaultlayout_gen(TITLE_PADDING = 50, PADDING = 30, BUTTON_X = (0.5,-95),BUTTON_WIDTH = (0,190)))
				
				title = Normal_Title(self, ABOUT_PAGE_TITLE)
				self.title = title
				
				text = Normal_FormattedText(self,ABOUT_PAGE_TEXT)
				self.doc = text
				
				confirm = Normal_Button(self, ABOUT_PAGE_CONFIRM_TEXT)
				self.button = confirm
				
				watch_ed = Normal_Button(self,ABOUT_PAGE_WATCH_ED_TEXT, ABOUT_PAGE_WATCH_ED_POS)
				self.sons.append(watch_ed)
				
				show_version_page = Normal_Button(self,ABOUT_PAGE_SHOW_VERSION_PAGE_TEXT,ABOUT_PAGE_SHOW_VERSION_PAGE_POS)
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
				
		# 成就信息
		class AchievementMessage(MessageInteractor,UIControl):
			def __init__(self, item):
				super(AchievementMessage,self).__init__((window,root,Posattr(*ACHIEVEMENT_MESSAGE_POS)),back = Sprite(normal_menu_back))
				icon = SpriteControl((window,self,Posattr(*ACHIEVEMENT_MESSAGE_ICON_POS)),Sprite(resource.load_image(item['icon'])))
				title = Normal_Title(self,item['name'],ACHIEVEMENT_MESSAGE_TITLE_POS)
				label = Normal_Title2(self,ACHIEVEMENT_MESSAGE_GOTTEN_TITLE if item['gotten'] else ACHIEVEMENT_MESSAGE_UNGOTTEN_TITLE,ACHIEVEMENT_MESSAGE_STATELABEL_POS)
				text = Normal_MessageText(self,item['text'] if item['gotten'] else item['cond'],ACHIEVEMENT_MESSAGE_TEXT_POS)
				confirm = Normal_Button(self,ACHIEVEMENT_MESSAGE_CONFIRM_TEXT,ACHIEVEMENT_MESSAGE_CONFIRM_POS)
				self.sons = (icon,title,label,text,confirm)
				self.submit_key = (confirm,'on_press')
				@self.event
				def on_submit():
					self.end()
		# 成就
		class AchievementPage(MessageInteractor,UIControl):
			def __init__(self):
				super(AchievementPage,self).__init__((window,root),back = Sprite(normal_page_back))
				
				achievement_tagpages = TagPages((window,self),layouter = TagPages_defaultlayoutV_gen(TAG_HEIGHT = ACHIEVEMENT_TAG_HEIGHT, TAG_PADDING = ACHIEVEMENT_TAG_PADDING, TAG_WIDTH = ACHIEVEMENT_TAG_WIDTH, FULL_PAGE = True))
				self.sons.append(achievement_tagpages)
				self.achievement_tagpages = achievement_tagpages
				
				achievement_page_title = Normal_Title0(self,ACHIEVEMENT_PAGE_TITLE,ACHIEVEMENT_PAGE_TITLE_POS)
				self.sons.append(achievement_page_title)
				self.achievement_page_title = achievement_page_title
				
				achievement_page_confirm = Normal_Button(self,ACHIEVEMENT_PAGE_CONFIRM_TEXT,ACHIEVEMENT_PAGE_CONFIRM_POS)
				self.sons.append(achievement_page_confirm)
				self.submit_key = (achievement_page_confirm,'on_press')
				self.achievement_page_confirm = achievement_page_confirm
				
				@self.event
				def on_show():
					self.refresh()
					self.on_resize()	
				@self.event
				def on_submit():
					self.end()
				
			def refresh(self):
				ACHIEVEMENT_VISIBLE_PAGES = []
				achievement_tagpages_pages = []
				achievement_tagpages_visible_id = {}
				ACHIEVEMENT_VISIBLE_ITEMS = []
				achievement_tagpages_items = []
				ACHIEVEMENT_PAGES = data.get_all_dict(['ACHIEVEMENT_PAGES'])
				ACHIEVEMENT_ITEMS = data.get_all_dict(['ACHIEVEMENT_ITEMS'])
				ACHIEVEMENT_PAGES_DATA = data.get_all_dict(['ACHIEVEMENT_PAGES_DATA'])
				ACHIEVEMENT_DATA = data.get_all_dict(['ACHIEVEMENT_DATA'])
				
				def achievement_tagpage_page_gen(item):
					button = Normal_Tag_rv(self.achievement_tagpages,item['name'])
					page = ImageFrame((window,self.achievement_tagpages,Posattr(*item['pos'])),back = Sprite(resource.load_image(item['background'])))
					return (button, page)
				def achievement_tagpage_item_gen(item):
					icon = resource.load_image(item['icon'])
					r = Button((window,achievement_tagpages_pages[achievement_tagpages_visible_id[item['page']]][1],Posattr(*item['pos'])),image = Sprite(icon),hover_color = NORMAL_BUTTON_HOVER_COLOR if item['gotten'] else ACHIEVEMENT_PAGE_ITEM_UNGOTTEN_HOVER_COLOR,
					color = NORMAL_BUTTON_COLOR if item['gotten'] else ACHIEVEMENT_PAGE_ITEM_UNGOTTEN_COLOR)
					@r.event
					def on_press():
						remove_sons(self)
						AchievementMessage(item).exe()
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
					self.achievement_tagpages.pages = achievement_tagpages_pages
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
				build_achievement_list()
				self.achievement_tagpages.page = 0
		# 附录（图鉴）
		class AppendicePage(MessageInteractor,UIControl):
			def __init__(self):
				super(AppendicePage,self).__init__((window,root),back = Sprite(normal_page_back))
				
				title = Normal_Title0(self,APPENDICE_PAGE_TITLE, APPENDICE_PAGE_TITLE_POS)
				self.sons.append(title)
				self.title = title
				
				confirm = Normal_Button(self,APPENDICE_PAGE_CONFIRM_TEXT,APPENDICE_PAGE_CONFIRM_POS)
				self.sons.append(confirm)
				self.confirm = confirm
				
				info = ImageFrame((window,self,Posattr(*APPENDICE_PAGE_INFO_POS)),back = Sprite(normal_menu_back))
				self.sons.append(info)
				self.info = info
				info_icon = SpriteControl((window,info,Posattr(*APPENDICE_PAGE_INFO_ICON_POS)),None)
				info_label = Normal_Title2(info, '',APPENDICE_PAGE_INFO_LABEL_POS)
				info_text = Normal_ScrollFormattedText(info,'',APPENDICE_PAGE_INFO_TEXT_POS)
				info.sons += (info_icon, info_label, info_text)
				self.info_icon = info_icon
				self.info_label = info_label
				self.info_text = info_text
				def info_refresh():
					self.info_text.scrollbar.rate = 0
					self.info.on_resize()
				info.refresh = info_refresh
				
				select = ImageFrame((window,self,Posattr(*APPENDICE_PAGE_SELECT_POS)),back = Sprite(normal_menu_back))
				self.select = select
				self.sons.append(select)
				select_list = ScrollFrame((window,select))
				self.select_list = select_list
				select.sons.append(select_list)
				
				select_scroll = Normal_ScrollBar(select_list)
				self.select_scroll = select_scroll
				select_list_buttons = SelectButtons((window,select_list),layouter = Grid_defaultlayout_gen(ITEM_HEIGHT = APPENDICE_PAGE_SELECT_ITEM_HEIGHT, ITEM_BLANKING = APPENDICE_PAGE_SELECT_ITEM_BLANKING, PADDING = 0))
				self.select_list_buttons = select_list_buttons
				select_list.frame = select_list_buttons
				select_list.scrollbar = select_scroll
				
				self.submit_key = (confirm,'on_press')
				@self.event
				def on_show():
					self.refresh()
					if len(self.APPENDICE_VISIBLE_ITEMS)==0:
						self.end()
						Alert_Notitle(APPENDICE_ITEMS_NONE_TEXT).exe()
				@self.event
				def on_submit():
					self.end()
			def refresh(self):
				APPENDICE_VISIBLE_ITEMS = []
				self.APPENDICE_VISIBLE_ITEMS = APPENDICE_VISIBLE_ITEMS
				select_list_items = []
				APPENDICE_ITEMS = data.get_all_dict(['APPENDICE_ITEMS'])
				APPENDICE_DATA = data.get_all_dict(['APPENDICE_DATA'])
				
				def select_list_items_gen(item):
					r = Normal_SwitchButton(self.select_list_buttons,item['name'])
					icon = Sprite(resource.load_image(item['icon']))
					r.icons = [icon,icon]
					return r
				
				def build_select_list():
					# 注意命名空间引发的问题
					APPENDICE_VISIBLE_ITEMS.clear()
					for (ky,value) in APPENDICE_ITEMS.items():
						if APPENDICE_DATA.get(ky,{}).get('visible',False):
							APPENDICE_VISIBLE_ITEMS.append(value)
					select_list_items.clear()
					select_list_items.extend([
						select_list_items_gen(i)
						for i in APPENDICE_VISIBLE_ITEMS
					])
					self.select_list_buttons.buttons = select_list_items
				
				@self.select_list_buttons.event
				def on_switch(id):
					if id < len(APPENDICE_VISIBLE_ITEMS):
						self.info_icon.image = Sprite(resource.load_image(APPENDICE_VISIBLE_ITEMS[id]['image']))
						self.info_label.text = APPENDICE_VISIBLE_ITEMS[id]['name']
						self.info_text.doc.doc = resource.decode_text(APPENDICE_VISIBLE_ITEMS[id]['text'])
					else:
						self.info_icon.image = None
						self.info_label.text = ''
						self.info_text.doc.doc = resource.default_formatted_text(APPENDICE_ITEMS_NONE_TEXT)
					self.info.refresh()
				
				build_select_list()
				self.select_scroll.rate = 0
				self.select_list_buttons.button = 0
				self.on_resize()
		
		# 剧本选择-开始游戏页面
		
		class ScenarioPage(MessageInteractor, UIControl):
			# _items_loaded = False
			def __init__(self):
				super(ScenarioPage, self).__init__((window,root),back = Sprite(normal_page_back))
				
				title = Normal_Title0(self,SCENARIO_PAGE_TITLE, SCENARIO_PAGE_TITLE_POS)
				self.sons.append(title)
				self.title = title
				
				confirm = Normal_Button(self,SCENARIO_PAGE_CONFIRM_TEXT,SCENARIO_PAGE_CONFIRM_POS)
				self.sons.append(confirm)
				self.confirm = confirm
				
				start_button = Normal_Button(self,SCENARIO_PAGE_START_TEXT,SCENARIO_PAGE_START_POS)
				self.sons.append(start_button)
				self.start_button = start_button
				
				info = ImageFrame((window,self,Posattr(*SCENARIO_PAGE_INFO_POS)),back = Sprite(normal_menu_back))
				info_icon = SpriteControl((window,info,Posattr(*SCENARIO_PAGE_INFO_ICON_POS)),None)
				info_label = Normal_Title2(info, '',SCENARIO_PAGE_INFO_LABEL_POS)
				info_text = Normal_ScrollFormattedText(info,'',SCENARIO_PAGE_INFO_TEXT_POS)
				info.sons += (info_icon, info_label, info_text)
				self.sons.append(info)
				self.info = info
				self.info_icon = info_icon
				self.info_label = info_label
				self.info_text = info_text
				
				select = ImageFrame((window,self,Posattr(*SCENARIO_PAGE_SELECT_POS)),back = Sprite(normal_menu_back))
				self.select = select
				self.sons.append(select)
				select_list = ScrollFrame((window,select))
				self.select_list = select_list
				select.sons.append(select_list)
				
				select_scroll = Normal_ScrollBar(select_list)
				self.select_scroll = select_scroll
				select_list_buttons = SelectButtons((window,select_list),layouter = Grid_defaultlayout_gen(ITEM_HEIGHT = SCENARIO_PAGE_SELECT_ITEM_HEIGHT, ITEM_BLANKING = SCENARIO_PAGE_SELECT_ITEM_BLANKING, PADDING = 0))
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
					if len(self.SCENARIO_VISIBLE_ITEMS)==0:
						alert_box = Alert_Notitle(SCENARIO_ITEMS_NONE_TEXT)
						@alert_box.event
						def on_submit():
							remove_control(self)
						alert_box.exe()
				@self.event
				def on_submit(id):
					self.end()
					if id != -1:
						scenario = self.SCENARIO_VISIBLE_ITEMS[id]
						play_game_from_scenario(scenario)
			# @property
			# def items_all(self):
				# if ScenarioPage._items_loaded:
					# return ScenarioPage._items_all
				# else:
					
					# ScenarioPage._items_loaded = True
			def refresh(self):
				SCENARIO_VISIBLE_ITEMS = []
				self.SCENARIO_VISIBLE_ITEMS = SCENARIO_VISIBLE_ITEMS
				select_list_items = []
				SCENARIOS = data.get_all_dict(['SCENARIOS'])
				SCENARIOS_DATA = data.get_all_dict(['SCENARIOS_DATA'])
				
				def select_list_items_gen(item):
					r = Normal_SwitchButton(self.select_list_buttons,item['name'])
					icon = Sprite(resource.load_image(item['icon']))
					r.icons = [icon,icon]
					return r
				def build_select_list():
					# 注意命名空间引发的问题
					SCENARIO_VISIBLE_ITEMS.clear()
					for (ky,value) in SCENARIOS.items():
						if SCENARIOS_DATA.get(ky,{}).get('visible',False):
							SCENARIO_VISIBLE_ITEMS.append(value)
					select_list_items.clear()
					select_list_items.extend([
						select_list_items_gen(i)
						for i in SCENARIO_VISIBLE_ITEMS
					])
					self.select_list_buttons.buttons = select_list_items
				@self.select_list_buttons.event
				def on_switch(id):
					if id < len(SCENARIO_VISIBLE_ITEMS):
						self.info_icon.image = Sprite(resource.load_image(SCENARIO_VISIBLE_ITEMS[id]['image']))
						self.info_label.text = SCENARIO_VISIBLE_ITEMS[id]['name']
						self.info_text.doc.doc = resource.decode_text(SCENARIO_VISIBLE_ITEMS[id]['text'])
					else:
						self.info_icon.image = None
						self.info_label.text = ''
						self.info_text.doc.doc = resource.default_formatted_text(SCENARIO_ITEMS_NONE_TEXT)
					self.info_text.scrollbar.rate = 0
					self.info.on_resize()
				build_select_list()
				self.select_scroll.rate = 0
				self.select_list_buttons.button = 0
				self.on_resize()
				
		# 主菜单
		class MainMenu(ImageFrame,UIControl):
			def __init__(self):
				super(MainMenu,self).__init__((window,root),back = Sprite(main_menu_back))
				start_button = Button(
					(window,self,Posattr(*MAIN_MENU_START_POS)),
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
					(window,self,Posattr(*pos)),
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
			def __init__(self, parent, pos = DEFAULT_POS):
				super(SavesBox, self).__init__((window, parent, Posattr(*pos)))
				
				select_list_buttons = SelectButtons((window,self),layouter = Grid_defaultlayout_gen(ITEM_HEIGHT = SAVESBOX_SELECT_ITEM_HEIGHT, ITEM_BLANKING = SAVESBOX_SELECT_ITEM_BLANKING, PADDING = 0))
				self.frame = select_list_buttons
				
				scrollbar = Normal_ScrollBar(self)
				self.scrollbar = scrollbar
			def refresh(self):
				self.SAVES = []
				self.select_list_items = []
				
				def select_list_items_gen(item):
					r = Normal_SwitchButton(self.frame,item)
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
				super(GamePageSave, self).__init__((window,root,Posattr(*SAVEPAGE_POS)), back = Sprite(normal_menu_back))
				self.gamepage = gamepage
				
				title = Normal_Title(self,SAVEPAGE_TITLE, SAVEPAGE_TITLE_POS)
				self.sons.append(title)
				self.title = title
				
				confirm_button = Normal_Button(self,SAVEPAGE_CONFIRM_TEXT,SAVEPAGE_CONFIRM_POS)
				self.sons.append(confirm_button)
				self.confirm_button = confirm_button
				
				delete_button = Normal_Button(self,SAVEPAGE_DEL_TEXT,SAVEPAGE_DEL_POS)
				self.sons.append(delete_button)
				self.delete_button = delete_button
				
				cancel = Normal_Button(self,SAVEPAGE_CANCEL_TEXT,SAVEPAGE_CANCEL_POS)
				self.sons.append(cancel)
				self.cancel = cancel
				self.submit_key = (cancel,'on_press')
				
				saves_box = SavesBox(self,SAVEPAGE_SELECT_POS)
				self.sons.append(saves_box)
				self.saves_box = saves_box
				
				name_label = Normal_Label(self, SAVEPAGE_NAME_LABEL_TEXT, SAVEPAGE_NAME_LABEL_POS)
				name = Normal_TextInput(self, '', SAVEPAGE_NAME_POS)
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
				saves.save(self.save_name, self.gamepage.game.gamedata)
				self.saves_box.refresh()
				self.end()
		class GamePageLoad(MessageInteractor, UIControl):
			def __init__(self):
				super(GamePageLoad, self).__init__((window,root,Posattr(*LOADPAGE_POS)), back = Sprite(normal_menu_back))
				
				title = Normal_Title(self,LOADPAGE_TITLE, LOADPAGE_TITLE_POS)
				self.sons.append(title)
				self.title = title
				
				confirm_button = Normal_Button(self,LOADPAGE_CONFIRM_TEXT,LOADPAGE_CONFIRM_POS)
				self.sons.append(confirm_button)
				self.confirm_button = confirm_button
				
				delete_button = Normal_Button(self,LOADPAGE_DEL_TEXT,LOADPAGE_DEL_POS)
				self.sons.append(delete_button)
				self.delete_button = delete_button
				
				cancel = Normal_Button(self,LOADPAGE_CANCEL_TEXT,LOADPAGE_CANCEL_POS)
				self.sons.append(cancel)
				self.cancel = cancel
				self.submit_key = (cancel,'on_press')
				
				saves_box = SavesBox(self,LOADPAGE_SELECT_POS)
				self.sons.append(saves_box)
				self.saves_box = saves_box
				
				checksum_label = Normal_Label(self, LOADPAGE_CHECKSUM_LABEL_TEXT, LOADPAGE_CHECKSUM_LABEL_POS)
				checksum = Normal_MessageText(self, '', LOADPAGE_CHECKSUM_POS)
				self.checksum_label = checksum_label
				self.checksum = checksum
				self.sons += (checksum, checksum_label)
				
				version_box = Normal_ScrollText(self, '', LOADPAGE_VERSION_POS)
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
						start_play()
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
				self.version = data.get('GAME_VERSION',GameVersion())
			save_data = property(lambda self:self._save_data,set_save_data)
		class GamePageMenu(MessageInteractor, UIControl):
			def __init__(self, gamepage):
				super(GamePageMenu, self).__init__((window,root,Posattr(*GAME_MENU_POS)), back = Sprite(normal_menu_back))
				
				title = Normal_Title(self,GAME_MENU_TITLE, GAME_MENU_TITLE_POS)
				self.title = title
				self.sons.append(title)
				
				buttons = Grid((window,self,Posattr(*GAME_MENU_BUTTONS_POS)), Grid_defaultlayout_gen(PADDING = 0))
				self.buttons = buttons
				self.sons.append(buttons)
				
				back_button = Normal_Button(self,GAME_MENU_BACK_TEXT)
				save_button = Normal_Button(self,GAME_MENU_SAVE_TEXT)
				achievement_button = Normal_Button(self,GAME_MENU_ACHIEVEMENT_TEXT)
				appendice_button = Normal_Button(self,GAME_MENU_APPENDICE_TEXT)
				setting_button = Normal_Button(self,GAME_MENU_SETTING_TEXT)
				quit_button = Normal_Button(self,GAME_MENU_QUIT_TEXT)
				
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
				super(GamePage,self).__init__((window, root))
				game = GamePlay(ui.data, ui, self, gamedata, load_from_save)
				self.game = game
				gamepage = self
				
				class GamePageHeader(ImageFrame):
					def __init__(self):
						super(GamePageHeader, self).__init__((window,gamepage,Posattr(*GAME_PAGE_HEADER_POS)), back = Sprite(game_page_header_back))
						gamepageheader = self
						class SpeedBar(Frame):
							def __init__(self):
								super(SpeedBar,self).__init__((window,gamepageheader,Posattr(*GAME_PAGE_HEADER_SPEEDBAR_POS)))
								speedbar = self
								
								slider = ButtonSlider((window,speedbar)
								,back = Sprite(game_page_header_speedbar_back))
								self.slider = slider
								self.sons.append(slider)
								class SliderButton(SwitchButton):
									def __init__(self):
										super(SliderButton,self).__init__((window,slider),images = [Sprite(game_page_header_speedbar_button_back),Sprite(game_page_header_speedbar_pressed_back)])
								slider.buttons = [
								SliderButton()
								for i in range( GAME_PAGE_HEADER_SPEEDBAR_COUNT)]
								slider.val = 0
								@slider.event
								def on_change(val):
									game.game_speed = val
								
								label = Label((window,self,Middle_Posattr()),pyglet.text.Label('',font_name = GAME_PAGE_HEADER_SPEEDBAR_FONT,font_size = GAME_PAGE_HEADER_SPEEDBAR_FONT_SIZE,color = GAME_PAGE_HEADER_SPEEDBAR_FONT_COLOR, anchor_x = 'center',anchor_y = 'center'))
								self.label = label
								self.sons.append(label)
							def refresh_label(self):
								self.label.text = (GAME_PAGE_HEADER_SPEEDBAR_PAUSE_TEXT if game.game_speed == 0 else '') + game.time.strftime(GAME_PAGE_HEADER_SPEEDBAR_TIME_FORMAT)
							def set_speed(self, v):
								self.slider._set_val(v)
								self.refresh_label()
						speedbar = SpeedBar()
						self.speedbar = speedbar
						self.sons.append(speedbar)
						
						class SwitchPageButtons(SelectButtons):
							def __init__(self):
								super(SwitchPageButtons,self).__init__((window,gamepageheader,Posattr(*GAME_PAGE_HEADER_SWITCH_PAGE_POS)),layouter = Grid_ratelayout_gen(COLUMNS = 4, ROWS = 1, PADDING = 0, ITEM_BLANKING = 0))
								switch_page_buttons = self
								
								class SwitchPageButton(SwitchButton):
									def __init__(self, icon_image, disabled_image = None):
										icon = Sprite(icon_image)
										selected_image = Sprite(game_header_switchpage_button_select_back)
										if disabled_image is not None:
											disabled_image = Sprite(disabled_image)
										super(SwitchPageButton,self).__init__((window,switch_page_buttons), icons = [icon,icon], images = [None,selected_image], disabled_images = None if disabled_image is None else [disabled_image,disabled_image], direction = 4)
								character_button = SwitchPageButton(game_header_character_icon)
								self.character_button = character_button
								timetable_button = SwitchPageButton(game_header_timetable_icon)
								self.timetable_button = timetable_button
								ability_button = SwitchPageButton(game_header_ability_icon)
								self.ability_button = ability_button
								contest_button = SwitchPageButton(game_header_contest_icon, game_header_contest_disabled_icon)
								self.contest_button = contest_button
								
								self.buttons = (character_button, timetable_button, ability_button, contest_button)
								@self.event
								def on_switch(id):
									gamepage.pages.page = id
						switch_page_buttons = SwitchPageButtons()
						self.switch_page_buttons = switch_page_buttons
						self.sons.append(switch_page_buttons)
						
						class StatusProgressBar(ProgressBar):
							def __init__(self, parent, color = (255,255,255), pos = DEFAULT_POS, label_text = None):
								_bar = Sprite(normal_progress_bar_front)
								_bar.color = color
								_back = Sprite(normal_progress_bar_back)
								_label = None
								if label_text is not None:
									_label = Normal_ValueLabel(label_text)
								super(StatusProgressBar,self).__init__((window,parent,Posattr(*pos)),label = _label,back = _back,bar = _bar)
						class StatusIconBars(Grid):
							def __init__(self, parent, pos):
								super(StatusIconBars,self).__init__((window, parent, Posattr(*pos)),layouter = Grid_ratelayout_gen(COLUMNS = 4,ROWS = 1,PADDING = 0,ITEM_BLANKING = 10))
								class StatusIconBar(StatusProgressBar):
									def __init__(self, parent, icon_image, color):
										icon = Sprite(icon_image)
										self.icon = icon
										super(StatusIconBar,self).__init__(parent, color)
									def on_resize(self):
										super(StatusIconBar,self).on_resize()
										self.resize_image_direction(self.icon, 4)
									def draw(self, range = None):
										# print('drawn a button')
										super(StatusIconBar, self).draw(range)
										if self.icon is not None:
											self.icon.draw()
								health_bar = StatusIconBar(self, game_header_bar_health_icon, GAME_HEADER_BAR_HEALTH_COLOR)
								self.health_bar = health_bar
								mood_bar = StatusIconBar(self, game_header_bar_mood_icon, GAME_HEADER_BAR_MOOD_COLOR)
								self.mood_bar = mood_bar
								stress_bar = StatusIconBar(self, game_header_bar_stress_icon, GAME_HEADER_BAR_STRESS_COLOR)
								self.stress_bar = stress_bar
								ability_bar = StatusIconBar(self, game_header_bar_ability_icon, GAME_HEADER_BAR_ABILITY_COLOR)
								self.ability_bar = ability_bar
					
								self.sons = (health_bar, mood_bar, stress_bar, ability_bar)
								self.relayout()
								
						status_bars = StatusIconBars(self, GAME_PAGE_HEADER_STATUS_BARS_POS)
						self.status_bars = status_bars
						self.sons.append(status_bars)
							
						rating_bar = StatusProgressBar(self,  GAME_PAGE_HEADER_RATING_BAR_DEFAULT_COLOR, GAME_PAGE_HEADER_RATING_BAR_POS, '')
						self.rating_bar = rating_bar
						self.sons.append(rating_bar)
						
						menu_button = Normal_Button(self,GAME_PAGE_HEADER_MENU_BUTTON_TEXT,GAME_PAGE_HEADER_MENU_BUTTON_POS)
						self.sons.append(menu_button)
						
						@menu_button.event
						def on_press():
							game.pause()
							GamePageMenu(gamepage).exe()
				
				header = GamePageHeader()
				self.header = header
				self.sons.append(header)
				
				class GamePages(MultiPage):
					def __init__(self):
						super(GamePages, self).__init__((window, gamepage, Posattr(*GAME_PAGES_POS)))
						
						class GamePages_Page(ImageFrame):
							def __init__(self, back_img):
								super(GamePages_Page,self).__init__((window,self),back = Sprite(back_img))
						character_page = GamePages_Page(game_pages_character_back)
						self.character_page = character_page
						
						timetable_page = GamePages_Page(game_pages_timetable_back)
						self.timetable_page = timetable_page
						
						ability_page = GamePages_Page(game_pages_ability_back)
						self.ability_page = ability_page
						
						contest_page = GamePages_Page(game_pages_contest_back)
						self.contest_page = contest_page
						
						self.pages = (character_page, timetable_page, ability_page, contest_page)
				
				pages = GamePages()
				self.pages = pages
				self.sons.append(pages)
				
				game.init_data()
			def set_speed(self, v):
				self.header.speedbar.set_speed(v)
			def refresh_time(self):
				self.header.speedbar.refresh_label()
			def refresh(self):
				pass
				# 刷新UI
			def exe(self):
				# 使用类名调用父类函数 -- 注意
				UIControl.exe(self)
				self.game.play()
				
		def play_game_from_scenario(scenario):
			gamedata = data.get(['GAME_DEFINE',scenario['game_define']])
			gamedata['SCENARIO_NAME'] = scenario['name']
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
		
		self.__dict__.update(locals())
	def set_fullscreen(self,v):
		self.window.set_fullscreen(v)
		self.data.set(['FULLSCREEN'],v)
	fullscreen = property(lambda self:self.window.fullscreen,set_fullscreen)
	def set_volume_music(self,v):
		self._volume_music = v
		self.data.set(['VOLUME_MUSIC'],v)
	volume_music = property(lambda self:self._volume_music,set_volume_music)
	def set_volume_effect(self,v):
		self._volume_effect = v
		self.data.set(['VOLUME_EFFECT'],v)
		# update volume
	volume_effect = property(lambda self:self._volume_effect,set_volume_effect)
	def set_volume_game(self,v):
		self._volume_game = v
		self.data.set(['VOLUME_GAME'],v)
		# update volume
	volume_game = property(lambda self:self._volume_game,set_volume_game)
	def show(self):
		self.window.show()