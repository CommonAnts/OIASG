#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pyglet

class Posattr(object):
	def __init__(self,x = (0,0), y = (0,0), width = (1,0), height = (1,0)):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
	def __call__(self,x,y,width,height):
		def c_h(p):
			return int(width*p[0]+p[1]+0.5)
		def c_v(p):
			return int(height*p[0]+p[1]+0.5)
		return x+c_h(self.x),y+c_v(self.y),c_h(self.width),c_v(self.height)
		
# 精灵（用于控件）
class Sprite(pyglet.sprite.Sprite):
	def show(self):
		self.visible = True
	def hide(self):
		self.visible = False
	def on_resize(self):
		pass
	@property
	def t_width(self):
		return self._texture.width
	@property
	def t_height(self):
		return self._texture.height
		
# 控件
class Control(pyglet.event.EventDispatcher):
	# x,y:控件位置
	# width,height:控件大小
	# visible:是否在显示
	def __init__(self, window = None, pos = Posattr(), x = 0, y = 0, width = 1, height = 1, absx = None, absy = None, abswidth = None, absheight = None, opacity = False):
		super(Control, self).__init__()
		self.opacity = opacity
		self.visible = False
		self.sons = []
		self.window = window
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.absx = absx
		self.absy = absy
		self.abswidth = abswidth
		self.absheight = absheight
		self.pos = pos
	# 碰撞检测：坐标是否在控件的矩形区域之内（严格）
	def set_abspos(self,abspos):
		self.x,self.y,self.width,self.height = abspos
		if self.absx is not None:
			self.x = self.absx
		if self.absy is not None:
			self.y = self.absy
		if self.abswidth is not None:
			self.width = self.abswidth
		if self.absheight is not None:
			self.height = self.absheight
		self.on_resize()
	abspos = property(lambda self:(self.x,self.y,self.width,self.height),set_abspos)
	def resize_label(self, label):
		if label is not None:
			label.x = int(self.x + self.width / 2 + 0.5)
			label.y = int(self.y + self.height / 2 + 0.5)
	def resize_image_full(self, image):
		if image is not None:
			image.update(x = self.x, y = self.y, scale_x = self.width / image.t_width, scale_y = self.height / image.t_height)
	def resize_image_direction(self, image, direction):
		if image is not None:
			if direction == 0:
				k = self.height / image.t_height
				image.update(x = self.x, y = self.y, scale = k)
			elif direction == 1:
				k = self.height / image.t_height
				image.update(x = self.x+self.width-k*self.icon.t_width, y = self.y, scale = k)
			elif direction == 2:
				k = self.width / image.t_width
				image.update(x = self.x, y = self.y+self.height-k*self.icon.t_height, scale = k)
			elif direction == 3:
				k = self.width / image.t_width
				image.update(x = self.x, y = self.y, scale = k)
			elif direction == 4:
				k = min(self.width / image.t_width, self.height / image.t_height)
				X = self.x + (self.width - k*image.t_width) / 2
				Y = self.y + (self.height - k*image.t_height) / 2
				image.update(x = X, y = Y, scale = k)
	def on_resize(self):
		pass
	def hit_test(self, x, y):
		return (self.x < x < self.x + self.width and
				self.y < y < self.y + self.height)
	def intersect(self,x,y,width,height):
		if x > self.x+self.width or self.x > x + width or y > self.y+self.height or self.y > y+height:
			return False
		return True
	# 显示和隐藏
	def show(self):
		# on_show在初始时触发
		self.dispatch_event('on_show')
		for i in self.sons:
			i.show()
		self.visible = True
	def hide(self):
		for i in self.sons:
			i.hide()
		self.visible = False
	def _draw(self, x):
		if x is not None:
			x.draw()
		return x is not None
	def draw(self, range = None):
		if range is None:
			x, y, width, height = self.x, self.y, self.width, self.height
		else:
			x, y, width, height = range
			x = max(x, self.x)
			y = max(y, self.y)
			width = min(width, self.x + self.width - x)
			height = min(height, self.y + self.height - y)
		for i in self.sons:
			if i.visible and i.intersect(x,y,width,height):
				i.draw((x,y,width,height))
	def on_mouse_press(self, x, y, button, modifiers):
		for j in range(len(self.sons)-1,-1,-1):
			i = self.sons[j]
			if i.visible and i.hit_test(x,y):
				i.on_mouse_press(x, y, button, modifiers)
				if not i.opacity:
					break
	def on_mouse_motion(self, x, y, dx, dy, shadowed = False):
		for j in range(len(self.sons)-1,-1,-1):
			i = self.sons[j]
			if i.visible:
				i.on_mouse_motion(x, y, dx, dy, shadowed)
				if i.hit_test(x,y) and not i.opacity:
					shadowed = True
	# 事件处理句柄：在点击激活控件后跟踪后续事件
	def capture_events(self):
		if self.window is not None:
			self.window.push_handlers(self)
	def release_events(self):
		if self.window is not None:
			self.window.remove_handlers(self)
	def on_show(self):
		pass
Control.register_event_type('on_show')

# 标签（用于控件）
class Label(Control):
	def __init__(self, control, label = None):
		super(Label, self).__init__(*control)
		self.label = label
		self.on_resize()
	def set_text(self, x):
		self.label.text = x
	text = property(lambda self:self.label.text,set_text)
	def on_resize(self):
		if self.label is not None:
			self.label.x = int(self.x + self.width / 2 + 0.5)
			self.label.y = int(self.y + self.height / 2 + 0.5)
		super(Label, self).on_resize()
	def draw(self, range = None):
		super(Label, self).draw(range)
		self._draw(self.label)

# 精灵控件
class SpriteControl(Control):
	def __init__(self, control, image = None, fixed_ratio = True):
		super(SpriteControl, self).__init__(*control)
		self.image = image
		self.fixed_ratio = fixed_ratio
		self.on_resize()
	def on_resize(self):
		super(SpriteControl, self).on_resize()
		if self.fixed_ratio:
			self.resize_image_direction(self.image, 4)
		else:
			self.resize_image_full(self.image)
	def draw(self, range = None):
		super(SpriteControl, self).draw(range)
		self._draw(self.image)

class Button(Control):
	# image:背景图片(Sprite类型)
	# icon:(左侧)图标(Sprite类型)
	# pressed_image:按下时的背景图片(Sprite类型)
	# label:文字(Lable/HTMLLable类型)
	# text:文字值
	# charged:是否被按下
	# direction:方向{0:图标靠左,1:图标靠右,2:图标靠上,3:图标靠下,4:图标居中}
	
	# 按钮于按下到松开之间获取事件控制句柄
	charged = False
	hovering = False
	def __init__(self, control, label = None, image = None, icon = None, pressed_image = None, direction = 0, color = (255,255,255), hover_color = (255,255,255), disabled_image = None):
		super(Button, self).__init__(*control)
		self.label = label
		self.image = image
		self.icon = icon
		self.pressed_image = pressed_image
		self.direction = direction
		self.hover_color = hover_color
		self.color = color
		self.disabled_image = disabled_image
		self.disabled = False
		self.on_resize()
	def set_text(self, x):
		self.label.text = x
	text = property(lambda self:self.label.text,set_text)
	# 注意舍入误差
	def on_resize(self):
		self.resize_image_full(self.image)
		self.resize_image_full(self.pressed_image)
		self.resize_image_full(self.disabled_image)
		self.resize_image_direction(self.icon, self.direction)
		self.resize_label(self.label)
			# self.label.height = None
			# self.label.width = None
		super(Button, self).on_resize()
	def _draw_image(self, image):
		if image is not None:
			if self.hovering:
				image.color = self.hover_color
			else:
				image.color = self.color
			image.draw()
		return image is not None
	def draw_image(self):
		if self.disabled:
			self._draw_image(self.disabled_image)
		else:
			if self.charged:
				if not self._draw_image(self.pressed_image):
					self._draw_image(self.image)
			else:
				self._draw_image(self.image)
	def draw(self, range = None):
		# print('drawn a button')
		super(Button, self).draw(range)
		self.draw_image()
		self._draw(self.label)
		if not self.disabled:
			self._draw(self.icon)
	def on_mouse_motion(self, x, y, dx, dy, shadowed = False):
		super(Button, self).on_mouse_motion(x, y, dx, dy, shadowed)
		self.hovering = not self.disabled and not shadowed and self.hit_test(x,y)
	def on_mouse_press(self, x, y, button, modifiers):
		# print('got mouse press')
		super(Button, self).on_mouse_press(x, y, button, modifiers)
		if not self.disabled:
			self.capture_events()
			self.dispatch_event('on_click')
			self.charged = True
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		# print('got mouse drag')
		self.charged = self.hit_test(x, y)
	def on_mouse_release(self, x, y, button, modifiers):
		# print('got mouse release')
		self.release_events()
		if not self.disabled:
			if self.hit_test(x, y):
				self.dispatch_event('on_press')
		self.charged = False
	def on_press(self):
		pass
	def on_click(self):
		pass
# on_press:从按钮松开时触发事件
Button.register_event_type('on_click')
Button.register_event_type('on_press')

# 多外观按钮
class SwitchButton(Button):
	def __init__(self, control, labels = None, images = None, icons = None, pressed_images = None, direction = 0, color = (255,255,255), hover_color = (255,255,255), disabled_images = None):
		super(SwitchButton, self).__init__(control)
		self.labels = labels
		self.images = images
		self.icons = icons
		self.pressed_images = pressed_images
		self.direction = direction
		self.hover_color = hover_color
		self.color = color
		self.disabled_images = disabled_images
		self.stage = 0
	def _get(self, x, id):
		if x is None:
			return None
		elif len(x) > id:
			return x[id]
		else:
			return None
	def on_switch(self, stage):
		pass
	def _set_stage(self, stage):
		# 不触发事件
		self._stage = stage
		self.label = self._get(self.labels,self.stage)
		self.image = self._get(self.images,self.stage)
		self.icon = self._get(self.icons,self.stage)
		self.pressed_image = self._get(self.pressed_images,self.stage)
		self.disabled_image = self._get(self.disabled_images,self.stage)
		self.on_resize()
	def set_stage(self, stage):
		self.dispatch_event('on_switch',stage)
		self._set_stage(stage)
	stage = property(lambda self:self._stage,set_stage)
SwitchButton.register_event_type('on_switch')

# 光标（不返回EVENT_HANDLED）
class Caret(pyglet.text.caret.Caret):
	def on_mouse_press(self, x, y, button, modifiers):
		super(Caret, self).on_mouse_press(x, y, button, modifiers)

# 文本框
class TextBox(Control):
	# text:pyglet.text.document.UnformattedDocumentl类型，表示文本
	# editable:是否允许编辑
	# multiline:是否多行
	# back:背景，Sprite类型
	
	# layout:文本
	# caret:光标(文本的)
	def __init__(self, control, text = None, style = None, editable = False, multiline = False, back = None, padding = 0, select_backcolor = None, select_textcolor = None, caret_color = None, valign = 'center'):
		super(TextBox, self).__init__(*control)
		if text is None:
			text = ''
		if style is None:
			style = {}
		self.doc = pyglet.text.document.UnformattedDocument(text)
		self.doc.set_style(0, len(self.doc.text), style)
		self.editable = editable
		self.back = back
		self.padding = padding
		self.layout = pyglet.text.layout.IncrementalTextLayout(
			self.doc, self.width-padding*2, self.height-padding*2, multiline)
		self.layout.content_valign = valign
		if select_backcolor is not None:
			self.layout.selection_background_color = select_backcolor
		if select_textcolor is not None:
			self.layout.selection_color = select_textcolor
		self.layout.x = self.x + padding
		self.layout.y = self.y + padding
		self.caret = None
		if self.editable:
			self.caret = Caret(self.layout,color = (caret_color if caret_color is not None else (style['color'][:3] if style.get('color') else (0,0,0))))
		self.on_resize()
	def set_text(self,x):
		self.doc.text = x
	text = property(lambda self:self.doc.text,set_text)
	def on_resize(self):
		if self.back is not None:
			self.back.update(x = self.x, y = self.y, scale_x = self.width / self.back.t_width , scale_y = self.height / self.back.t_height)
		if self.layout is not None:
			self.layout.x = self.x + self.padding
			self.layout.y = self.y + self.padding
			self.layout.width = self.width-self.padding*2
			self.layout.height = self.height-self.padding*2
		super(TextBox, self).on_resize()
		self.dispatch_event('on_layout_update')
	def draw(self, range = None):
		super(TextBox, self).draw(range)
		self._draw(self.back)
		self._draw(self.layout)
	def on_mouse_press(self, x, y, button, modifiers):
		# print('got mouse press')
		super(TextBox, self).on_mouse_press(x, y, button, modifiers)
		if self.window is not None and self.caret is not None:
			self.window.push_handlers(self.caret)
TextBox.register_event_type('on_layout_update')
			
class FormattedTextBox(TextBox):
	def __init__(self, control, doc = None, editable = False, multiline = False, back = None, padding = 0, select_backcolor = None, select_textcolor = None, caret_color = None, valign = 'center'):
		super(TextBox, self).__init__(*control)
		self.editable = editable
		self.back = back
		self.padding = padding
		self.multiline = multiline
		self.layout = None
		self.doc = doc
		self.layout.content_valign = valign
		self.layout.x = self.x + padding
		self.layout.y = self.y + padding
		
		if select_backcolor is not None:
			self.layout.selection_background_color = select_backcolor
		if select_textcolor is not None:
			self.layout.selection_color = select_textcolor
		self.caret = None
		if self.editable:
			self.caret = Caret(self.layout,color = (caret_color if caret_color is not None else (0,0,0)))
		self.on_resize()
	def set_doc(self, doc):
		self._doc = doc
		if doc is not None:
			self.layout = pyglet.text.layout.IncrementalTextLayout(
			self.doc, self.width-self.padding*2, self.height-self.padding*2, self.multiline)
			self.dispatch_event('on_layout_update')
	doc = property(lambda self:self._doc,set_doc)

# 视频播放器
class MediaPlayer(Control):
	def __init__(self,control,player = None,loop = False):
		super(MediaPlayer,self).__init__(*control)
		self.player = player
		self.loop = loop
	def draw(self, range = None):
		super(MediaPlayer, self).draw(range)
		if self.player is not None:
			t = self.player.get_texture()
			if t is not None:
				t.blit(self.x,self.y,width = self.width,height = self.height)
	def clear(self):
		self.pause()
		self.player = None
	def set_player(self,player):
		self._player = player
		if player is not None:
			def f(event,selfevent):
				def g(*args, **kw):
					self.dispatch_event(selfevent)
				return g
			player.on_eos = f(player.on_eos,'on_eos')
			player.on_player_eos = f(player.on_player_eos,'on_player_eos')
			player.loop = self.loop
	player = property(lambda self:self._player,set_player)
	def play(self):
		if self.player is not None:
			self.player.play()
	def pause(self):
		if self.player is not None:
			self.player.pause()
	def seek(self,val):
		if self.player is not None:
			self.player.seek(val)
	def rewind(self):
		self.seek(0)
	def queue(self,source):
		if self.player is not None:
			self.player.queue(source)
	def set_volume(self,volume):
		if self.player is not None:
			self.player.volume = volume
	volume = property(lambda self:self.player.volume if self.player is not None else None,set_volume)
	def set_loop(self,loop):
		self._loop = loop
		if self.player is not None:
			self.player.loop = loop
	loop = property(lambda self:self._loop,set_loop)
	def on_mouse_press(self, x, y, button, modifiers):
		super(MediaPlayer, self).on_mouse_press(x, y, button, modifiers)
		self.dispatch_event('on_press')
	def on_eos(self):
		pass
	def on_player_eos(self):
		pass
	def on_press(self):
		pass
MediaPlayer.register_event_type('on_eos')
MediaPlayer.register_event_type('on_player_eos')
MediaPlayer.register_event_type('on_press')

# 进度条
class ProgressBar(Control):
	# label:文字标签
	# back:背景图片
	# bar:进度条图片（注意：缩放）
	# bar_sizerate:进度条图片占比（left,bottom,width,height，以比例计）
	# direction:{0:从左到右,1:从右到左,2:从下到上,3:从上到下}
	def __init__(self, control, label = None, back = None, bar = None, bar_sizerate = (0,0,1,1), direction = 0, rate = 1):
		super(ProgressBar, self).__init__(*control)
		self.label = label
		self.back = back
		self.bar = bar
		self.bar_sizerate = bar_sizerate
		self.direction = direction
		self.rate = rate
	def set_rate(self, x):
		self._rate = x
		self.on_resize()
	rate = property(lambda self:self._rate,set_rate)
	def on_resize(self):
		self.resize_image_full(self.back)
		if self.bar is not None:
			K = self.bar_sizerate
			ra = self._rate
			L,R,U,D = self.x + self.width*K[0],self.x + self.width*(K[0]+K[2]),self.y + self.height*(K[1]+K[3]),self.y + self.height*K[1]
			if self.direction == 0:
				self.bar.update(x = L, y = D, scale_x = (R-L)*ra/self.bar.t_width, scale_y = (U-D)/self.bar.t_height)
			elif self.direction == 1:
				self.bar.update(x = int(R-(R-L)*ra/self.bar.t_width+0.5), y = D, scale_x = (R-L)*ra/self.bar.t_width, scale_y = (U-D)/self.bar.t_height)
			elif self.direction == 2:
				self.bar.update(x = L, y = D, scale_x = (R-L)/self.bar.t_width, scale_y = (U-D)*ra/self.bar.t_height)
			elif self.direction == 3:
				self.bar.update(x = L, y = int(U-(U-D)*ra/self.height+0.5), scale_x = (R-L)/self.bar.t_width, scale_y = (U-D)*ra/self.bar.t_height)
		self.resize_label(self.label)
		super(ProgressBar, self).on_resize()
	def set_text(self,x):
		self.label.text = x
	text = property(lambda self:self.label.text,set_text)
	def draw(self, range = None):
		super(ProgressBar, self).draw(range)
		self._draw(self.back)
		self._draw(self.bar)
		self._draw(self.label)

# 水平滚动条	
class Slider(Control):
	# image:背景图片(Sprite类型)
	# cursor:游标(Sprite类型)
	
	# 游标于按下到松开之间获取事件控制句柄
	def __init__(self, control, image = None, cursor = None, rate = 0):
		super(Slider, self).__init__(*control)
		self.image = image
		self.cursor = cursor
		self.rate = rate
	def _set_rate(self, x):
		x = max(0,min(x,1))
		self._rate = x
		self.on_resize()
	def set_rate(self, x):
		self._set_rate(x)
		self.dispatch_event('on_change', self.rate)
	rate = property(lambda self:self._rate,set_rate)
	def on_resize(self):
		if self.image is not None:
			self.image.update(x = self.x, y = int(self.y + self.height/2 - self.image.t_height/2+0.5), scale_x = self.width / self.image.t_width)
		if self.cursor is not None:
			k = self.height / self.cursor.t_height
			self.cursor.update(x = self.x + self.rate*(self.width - k * self.cursor.t_width), y = self.y, scale = k)
		super(Slider, self).on_resize()
	def draw(self, range = None):
		super(Slider, self).draw(range)
		self._draw(self.image)
		self._draw(self.cursor)
	def on_mouse_press(self, x, y, button, modifiers):
		# print('got mouse press')
		super(Slider, self).on_mouse_press(x, y, button, modifiers)
		self.rate = (x-self.x-self.cursor.width/2)/max(1,self.width-self.cursor.width)
		self.capture_events()
		self.dispatch_event('on_begin_scroll')
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.rate = (x-self.x-self.cursor.width/2)/max(1,self.width-self.cursor.width)
	def on_mouse_release(self, x, y, button, modifiers):
		self.release_events()
		self.dispatch_event('on_end_scroll')
	def on_change(self,val):
		# print(val)
		pass
	def on_begin_scroll(self):
		pass
	def on_end_scroll(self):
		pass

Slider.register_event_type('on_begin_scroll')
Slider.register_event_type('on_end_scroll')
Slider.register_event_type('on_change')
	
# 垂直滚动条
class ScrollBar(Slider):
	def on_resize(self):
		if self.image is not None:
			self.image.update(x = int(self.x + self.width/2 - self.image.t_width/2+0.5), y = self.y, scale_y = self.height / self.image.t_height)
		if self.cursor is not None:
			k = self.width / self.cursor.t_width
			self.cursor.update(x = self.x, y = self.y + (1-self.rate)*(self.height - k * self.cursor.t_height), scale = k)
		super(Slider, self).on_resize()
	def on_mouse_press(self, x, y, button, modifiers):
		# print('got mouse press')
		super(Slider, self).on_mouse_press(x, y, button, modifiers)
		self.rate = 1-(y-self.y-self.cursor.height/2)/max(1,self.height-self.cursor.height)
		self.capture_events()
		self.dispatch_event('on_begin_scroll')
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.rate = 1-(y-self.y-self.cursor.height/2)/max(1,self.height-self.cursor.height)

# 框架（控件组及布局容器）
class Frame(Control):
	def __init__(self, control, x_base = 0, y_base = 0):
		super(Frame, self).__init__(*control)
		self._x_base = x_base
		self._y_base = y_base
		self.on_resize()
	def _on_resize(self):
		for i in self.sons:
			i.abspos = i.pos(self.x + self.x_base,self.y + self.y_base,self.width,self.height)
			i.on_resize()
	def on_resize(self):
		self._on_resize()
		super(Frame, self).on_resize()
		self.dispatch_event('on_frame_resize')
	def on_frame_resize(self):
		pass
	def set_x_base(self,x_base):
		self._x_base = x_base
		self._on_resize()
	x_base = property(lambda self:self._x_base,set_x_base)
	def set_y_base(self,y_base):
		self._y_base = y_base
		self._on_resize()
	y_base = property(lambda self:self._y_base,set_y_base)

# 视口
class Viewport(Frame):
	def __init__(self, control, x_base = 0, y_base = 0):
		super(Viewport, self).__init__(control, x_base, y_base)
		self.on_resize()
	def draw(self, range = None):
		t = pyglet.image.get_buffer_manager().get_color_buffer().get_texture()
		super(Viewport, self).draw(range)
		f = pyglet.image.get_buffer_manager().get_color_buffer().get_region(self.x,self.y,self.width,self.height).get_texture()
		t.blit(0,0)
		f.blit(self.x,self.y)
Viewport.register_event_type('on_frame_resize')
		
# 多页面
class MultiPage(Frame):
	def __init__(self, control, pages = None):
		super(MultiPage, self).__init__(control)
		self.pages = pages if pages is not None else []
	def set_pages(self, pages):
		# print('set_buttons')
		self._pages = pages
		self.sons = pages
		self.page = 0
	pages = property(lambda self:self._pages,set_pages)
	def set_page(self, page):
		self._page = page
		for i in range(len(self.pages)):
			if i == page:
				if self.visible:
					self.pages[i].show()
			else:
				self.pages[i].hide()
		self.dispatch_event('on_switch',self.page)
	page = property(lambda self:self._page,set_page)
	def show(self):
		super(MultiPage, self).show()
		for i in range(len(self.pages)):
			if i != self.page:
				self.pages[i].hide()
	def on_switch(self, page):
		# print('on switch:%d' % page)
		pass
MultiPage.register_event_type('on_switch')

# 自动布局框架
class LayoutFrame(Frame):
	_layouter = None
	def relayout(self):
		self.layouter(self)
	def set_layouter(self, layouter):
		self._layouter = layouter
		self.relayout()
	layouter = property(lambda self:self._layouter,set_layouter)

def Grid_defaultlayout_gen(COLUMNS = 1, PADDING = 20, ITEM_BLANKING = 10, ITEM_HEIGHT = 30, ITEM_WIDTH = None, CAL_ABSH = True):
	def Grid_defaultlayout(self):
		if not self.sons:
			return
		ROWS = (len(self.sons)+COLUMNS-1)//COLUMNS
		if ITEM_WIDTH is None:
			item_wk = 1/COLUMNS
			item_wb = -(ITEM_BLANKING*(COLUMNS-1)+PADDING*2)/COLUMNS
		else:
			item_wk = 0
			item_wb = ITEM_WIDTH
		if ITEM_HEIGHT is None:
			item_hk = 1 / ROWS
			item_hb = -(ITEM_BLANKING*(ROWS-1)+PADDING*2) / ROWS
		else:
			item_hk = 0
			item_hb = ITEM_HEIGHT
		cur_xk, cur_xb = 0, PADDING
		cur_yk, cur_yb = 1 - item_hk, - item_hb - PADDING
		for i in range(len(self.sons)):
			self.sons[i].pos = Posattr((cur_xk,cur_xb),(cur_yk,cur_yb),(item_wk,item_wb),(item_hk,item_hb))
			if (i+1)%COLUMNS == 0:
				cur_xk , cur_xb = 0, PADDING
				cur_yk -= item_hk
				cur_yb -= ITEM_BLANKING + item_hb
			else:
				cur_xk += item_wk
				cur_xb += item_wb + ITEM_BLANKING
		if ITEM_WIDTH is None:
			self.abswidth = None
		else:
			columns = min(len(self.sons),COLUMNS)
			self.abswidth = columns*ITEM_WIDTH + (columns-1)*ITEM_BLANKING + 2*PADDING
		if ITEM_HEIGHT is None or not CAL_ABSH:
			self.absheight = None
		else:
			self.absheight = ROWS*ITEM_HEIGHT + (ROWS-1)*ITEM_BLANKING + 2*PADDING
	return Grid_defaultlayout

Grid_defaultlayout = Grid_defaultlayout_gen()

def Grid_ratelayout_gen(COLUMNS = 1, ROWS = 1, PADDING = 20, ITEM_BLANKING = 10):
	def Grid_ratelayout(self):
		if not self.sons:
			return
		item_wk = 1 / COLUMNS
		item_wb = -(ITEM_BLANKING*(COLUMNS-1)+PADDING*2) / COLUMNS
		item_hk = 1 / ROWS
		item_hb = -(ITEM_BLANKING*(ROWS-1)+PADDING*2) / ROWS
		cur_xk, cur_xb, cur_yk, cur_yb = 0, PADDING, 1-item_hk, -item_hb-PADDING
		for i in range(len(self.sons)):
			self.sons[i].pos = Posattr((cur_xk,cur_xb),(cur_yk,cur_yb),(item_wk,item_wb),(item_hk,item_hb))
			if (i+1)%COLUMNS == 0:
				cur_xk , cur_xb = 0, PADDING
				cur_yk -= item_hk
				cur_yb -= ITEM_BLANKING + item_hb
			else:
				cur_xk += item_wk
				cur_xb += item_wb + ITEM_BLANKING
	return Grid_ratelayout

class Grid(LayoutFrame):
	def __init__(self,control,layouter = Grid_defaultlayout):
		super(Grid, self).__init__(control)
		self.layouter = layouter
	
class LRButtons(Grid):
	def __init__(self, control, buttons = None):
		super(LRButtons, self).__init__(control, layouter = Grid_ratelayout_gen(ROWS = 1,COLUMNS = 2, PADDING = 0, ITEM_BLANKING = 0))
		self.sons = buttons if buttons is not None else []
		self.relayout()
	
class UDButtons(Grid):
	def __init__(self, control, buttons = None):
		super(UDButtons, self).__init__(control, layouter = Grid_ratelayout_gen(ROWS = 2,COLUMNS = 1, PADDING = 0, ITEM_BLANKING = 0))
		self.sons = buttons if buttons is not None else []
		self.relayout()
	
class SelectButtons(Grid):
	def __init__(self, control, buttons = None, layouter = Grid_defaultlayout, canceling = False):
		super(SelectButtons, self).__init__(control, layouter)
		self.layouter = layouter
		self.canceling = canceling
		self.buttons = buttons if buttons is not None else []
	def set_buttons_event(self):
		for i in range(len(self.buttons)):
			def g(i):
				def f():
					if self.canceling and self.button == i:
						self.button = -1
					else:
						self.button = i
				return f
			self.buttons[i].on_press = g(i)
	def insert(self, button):
		if button not in self.buttons:
			self.buttons.append(button)
		if button not in self.sons:
			self.sons.append(button)
		self.set_buttons_event()
		self.relayout()
		self.button = 0
	def remove(self, button):
		self.buttons.remove(button)
		self.sons.remove(button)
		self.set_buttons_event()
		self.relayout()
		self.button = 0
	def _set_buttons(self, buttons):
		self._buttons = buttons
		self.sons = buttons
		self.set_buttons_event()
		self.relayout()
	def set_buttons(self, buttons):
		self._set_buttons(buttons)
		self.button = 0
	buttons = property(lambda self:self._buttons,set_buttons)
	def _set_button(self, button):
		self._button = button
		for i in range(len(self.buttons)):
			if i == button:
				self.buttons[i].stage = 1
			else:
				self.buttons[i].stage = 0
	def set_button(self, button):
		self._set_button(button)
		self.dispatch_event('on_switch',self.button)
	button = property(lambda self:self._button,set_button)
	def on_switch(self, button):
		pass
SelectButtons.register_event_type('on_switch')
	
# 图片框架
class ImageFrame(Frame):
	# back:背景图片(AbstractImage)
	# front:前景图片(AbstractImage)
	def __init__(self, control, back = None, front = None):
		self.back = back
		self.front = front
		super(ImageFrame, self).__init__(control)
	def draw(self, range = None):
		self._draw(self.back)
		super(ImageFrame, self).draw(range)
		self._draw(self.front)
	def on_resize(self):
		self.resize_image_full(self.back)
		self.resize_image_full(self.front)
		super(ImageFrame, self).on_resize()

class ImageLayoutFrame(ImageFrame,LayoutFrame):
	def __init__(self, control, back = None, front = None, layouter = lambda self:None):
		super(ImageLayoutFrame, self).__init__(control,back,front)
		self.layouter = layouter
			
def ScrollTextBox_defaultlayout_gen(SCROLL_BAR_WIDTH = 20, COVER = False):
	def f(self):
		if self.scrollbar is not None:
			self.scrollbar.pos = Posattr((1,-SCROLL_BAR_WIDTH),(0,0),(0,SCROLL_BAR_WIDTH),(1,0))
		if self.doc is not None:
			self.doc.pos = Posattr((0,0),(0,0),(1,0 if COVER else -SCROLL_BAR_WIDTH),(1,0))
	return f
ScrollTextBox_defaultlayout = ScrollTextBox_defaultlayout_gen()

# 可滚动的文本框
# 需要保证doc在scrollbar之前设置
class ScrollTextBox(LayoutFrame):
	def __init__(self, control, doc = None, scrollbar = None, layouter = ScrollTextBox_defaultlayout):
		self._layouter = layouter
		self._doc = doc
		self._scrollbar = scrollbar
		super(ScrollTextBox, self).__init__(control)
		self.doc = doc
		self.scrollbar = scrollbar
		self.layouter = layouter
		self.on_resize()
		self.check_scroll()
	iskey = lambda self, x: x is self.scrollbar or x is self.doc
	def set_text(self,x):
		if self.doc is not None:
			self.doc.text = x
		self.check_scroll()
	text = property(lambda self:self.doc.text if self.doc is not None else None,set_text)
	def set_doc(self,doc):
		self._doc = doc
		if doc is not None:
			if doc not in self.sons:
				self.sons.append(doc)
			@self.doc.event
			def on_layout_update():
				self.check_scroll()
		self.sons = list(filter(self.iskey,self.sons))
		self.relayout()
		self.check_scroll()
	doc = property(lambda self:self._doc, set_doc)
	def set_scrollbar(self,scrollbar):
		self._scrollbar = scrollbar
		if scrollbar is not None:
			if scrollbar not in self.sons:
				self.sons.append(scrollbar)
			if self.doc is not None and self.doc.layout is not None:
				@scrollbar.event
				def on_change(rate):
					self.doc.layout.ensure_line_visible(min(max(int(rate*self.doc.layout.get_line_count()),0),self.doc.layout.get_line_count()-1))
		self.sons = list(filter(self.iskey,self.sons))
		self.relayout()
		self.check_scroll()
	scrollbar = property(lambda self:self._scrollbar,set_scrollbar)
	def check_scroll(self):
		# 判定滚动条是否需要
		if self.scrollbar is None:
			return
		if self.doc is None:
			self.scrollbar.hide()
		# 比较行基线 -- 可能会导致末尾行显示不全（因为基线不在行下方），待解决
		if self.doc.layout.get_point_from_line(self.doc.layout.get_line_count()-1)[1] >= 0 and self.scrollbar.rate == 0:
			if self.scrollbar.visible:
				self.scrollbar.hide()
		else:
			if self.visible and not self.scrollbar.visible:
				self.scrollbar.show()
	def show(self):
		# on_show在初始时触发
		self.dispatch_event('on_show')
		for i in self.sons:
			i.show()
		self.visible = True
		self.check_scroll()
	def on_resize(self):
		super(LayoutFrame, self).on_resize()
		self.check_scroll()

def ScrollFrame_defaultlayout_gen(SCROLL_BAR_WIDTH = 20, COVER = True):
	def f(self):
		if self.scrollbar is not None:
			self.scrollbar.pos = Posattr((1,-SCROLL_BAR_WIDTH),(0,0),(0,SCROLL_BAR_WIDTH),(1,0))
		if self._viewport is not None:
			self._viewport.pos = Posattr((0,0),(0,0),(1,0 if COVER else -SCROLL_BAR_WIDTH),(1,0))
	return f
ScrollFrame_defaultlayout = ScrollFrame_defaultlayout_gen()

# 可滚动的框架
# 注意：这里的 frame 是越级访问
# 需要保证frame在scrollbar之前设置
class ScrollFrame(LayoutFrame):
	def __init__(self, control, frame = None, scrollbar = None, layouter = ScrollFrame_defaultlayout):
		self._viewport = Viewport((control[0],self))
		self._scrollbar = scrollbar
		self._frame = frame
		self._layouter = layouter
		super(ScrollFrame, self).__init__(control)
		self.sons.append(self._viewport)
		self.scrollbar = scrollbar
		self.frame = frame
		self.layouter = layouter
		self.on_resize()
		self.check_scroll()
	isselfframe = lambda self, x: x is self.frame
	iskey = lambda self, x: x is self.scrollbar or x is self._viewport
	def set_frame(self,frame):
		self._frame = frame
		if frame is not None:
			if frame not in self._viewport.sons:
				self._viewport.sons.append(frame)
			frame.pos = Posattr()
		self._viewport.sons = list(filter(self.isselfframe,self._viewport.sons))
		self.relayout()
		self.check_scroll()
	frame = property(lambda self:self._frame, set_frame)
	def set_scrollbar(self,scrollbar):
		self._scrollbar = scrollbar
		if scrollbar is not None:
			if scrollbar not in self.sons:
				self.sons.append(scrollbar)
			if self.frame is not None:
				def _viewport_setbase(rate):
					d = self._viewport.height - self.frame.height
					if d >= 0:
						self._viewport.y_base = d
					else:
						self._viewport.y_base = d*rate
				@self._viewport.event
				def on_frame_resize():
					_viewport_setbase(1-self.scrollbar.rate)
				@self.scrollbar.event
				def on_change(rate):
					_viewport_setbase(1-rate)
		self.sons = list(filter(self.iskey,self.sons))
		self.relayout()
		self.check_scroll()
	scrollbar = property(lambda self:self._scrollbar,set_scrollbar)
	def check_scroll(self):
		# 判定滚动条是否需要
		if self.scrollbar is None:
			return
		if self.frame is None:
			self.scrollbar.hide()
		# 比较行基线 -- 可能会导致末尾行显示不全（因为基线不在行下方），待解决
		if self._viewport.height >= self.frame.height and self.scrollbar.rate == 0:
			if self.scrollbar.visible:
				self.scrollbar.hide()
		else:
			if self.visible and not self.scrollbar.visible:
				self.scrollbar.show()
	def show(self):
		# on_show在初始时触发
		self.dispatch_event('on_show')
		for i in self.sons:
			i.show()
		self.visible = True
		self.check_scroll()
	def on_resize(self):
		super(LayoutFrame, self).on_resize()
		self.check_scroll()
		
def ButtonSlider_defaultlayout_gen(PADDING_RATE = 0.2, HPADDING_RATE = 0.5, VPADDING_RATE = 0.15):
	def f(self):
		if len(self.sons) == 0:
			return
		else:
			rate = 1/(len(self.sons)*(1+PADDING_RATE)-PADDING_RATE+2*HPADDING_RATE)
			padding_rate = PADDING_RATE * rate
			hpadding_rate = HPADDING_RATE * rate
			cur_t = hpadding_rate
			for i in self.sons:
				i.pos = Posattr((cur_t,0),(VPADDING_RATE,0),(rate,0),(1-VPADDING_RATE*2,0))
				cur_t += rate + padding_rate
	return f
ButtonSlider_defaultlayout = ButtonSlider_defaultlayout_gen()
	
# 按钮条
class ButtonSlider(ImageFrame, LayoutFrame):
	def __init__(self, control, back = None, front = None, buttons = None, layouter = ButtonSlider_defaultlayout):
		super(ButtonSlider, self).__init__(control, back, front)
		self.layouter = layouter
		self.val = 0
		if buttons is not None:
			self.buttons = buttons
	def set_buttons(self, v):
		# print('set_buttons')
		self.sons = v
		for i in range(len(self.sons)):
			def g(i):
				def f():
					self.val = i
				return f
			self.sons[i].on_press = g(i)
		self.relayout()
	buttons = property(lambda self:self.sons,set_buttons)
	def _set_val(self, v):
		self._val = v
		for i in range(min(v+1,len(self.sons))):
			self.sons[i].stage = 0
		for i in range(v+1,len(self.sons)):
			self.sons[i].stage = 1
	def set_val(self, v):
		self._set_val(v)
		self.dispatch_event('on_change',self._val)
	val = property(lambda self:self._val,set_val)
	def on_change(self, val):
		pass
ButtonSlider.register_event_type('on_change')

# 交互式事件窗口
class MessageInteractor(ImageFrame):
	_TIED_KEY_VAR = '_tied_MessageInteractor_event_'
	# key_event 和 key_events 不可同时使用
	def set_submit_key_event(self, event):
		obj, eventname = event
		# print('set_submit_key_event')
		if not getattr(obj, self._TIED_KEY_VAR + eventname, False):
			setattr(obj, self._TIED_KEY_VAR + eventname, True)
			def f(event):
				def g(*args, **kw):
					self.dispatch_event('on_submit')
					# print('on_submit_')
					return event(*args, **kw)
				return g
			setattr(obj, eventname ,f(getattr(obj, eventname)))
		self._submit_key = getattr(obj, eventname)
	submit_key = property(lambda self:self._submit_key,set_submit_key_event)
	def set_submit_key_events(self, events):
		self._submit_keys = []
		for i in range(len(events)):
			event = events[i]
			obj, eventname = event
			if not getattr(obj, self._TIED_KEY_VAR + eventname, False):
				setattr(obj, self._TIED_KEY_VAR + eventname, True)
				def f(event, id):
					def g(*args, **kw):
						self.dispatch_event('on_submit', id)
						return event(*args, **kw)
					return g
				setattr(obj, eventname ,f(getattr(obj, eventname), i))
			self._submit_keys.append(getattr(obj, eventname))
	submit_keys = property(lambda self:self._submit_keys,set_submit_key_events)
	def on_submit(*args,**kw):
		self = args[0]
		# print('on_submit')
		self.hide()
	
MessageInteractor.register_event_type('on_submit')

def AlertBox_defaultlayout_gen(BUTTON_HEIGHT = 30, BUTTON_BLANKING = 10, PADDING = 20, TITLE_PADDING = 20, TITLE_HEIGHT = 30, BUTTON_X = (0.2,20), BUTTON_WIDTH = (0.6,-40)):
	def f(self):
		if self.title is not None:
			self.title.pos = Posattr((0.5,0),(1,-TITLE_PADDING-TITLE_HEIGHT/2),(0,0),(0,0))
		cur_h = PADDING
		if self.button is not None:
			self.button.pos = Posattr(BUTTON_X,(0,cur_h),BUTTON_WIDTH,(0,BUTTON_HEIGHT))
		cur_h += BUTTON_HEIGHT + BUTTON_BLANKING
		if self.doc is not None:
			self.doc.pos = Posattr((0,PADDING),(0,cur_h),(1,-2*PADDING),(1,-cur_h-TITLE_PADDING-TITLE_HEIGHT))
	return f
AlertBox_defaultlayout = AlertBox_defaultlayout_gen()

class AlertBox(MessageInteractor, LayoutFrame):
	def __init__(self, control, back = None, front = None, title = Label(()),  doc = None, button = None, layouter = AlertBox_defaultlayout):
		super(AlertBox, self).__init__(control, back, front)
		self._layouter = layouter
		self._title = None
		self._doc = None
		self._button = None
		self.title = title
		self.doc = doc
		self.button = button
		self.relayout()
		self.on_resize()
	# 注意：请不要多次设置button，否则可能导致on_submit事件触发多次
	iskey = lambda self, x: x is self.title or x is self.doc or x is self.button
	def set_button(self, button):
		self._button = button
		if button is not None:
			if button not in self.sons:
				self.sons.append(button)
			self.submit_key = (button, 'on_press')
		self.sons = list(filter(self.iskey,self.sons))
		self.relayout()
	button = property(lambda self:self._button, set_button)
	def set_text(self,x):
		if self.doc is not None:
			self.doc.text = x
	text = property(lambda self:self.doc.text if self.doc is not None else None,set_text)
	def set_title_text(self,x):
		if self.title is not None:
			self.title.text = x
	title_text = property(lambda self:self.title.text if self.title is not None else None,set_title_text)
	def set_title(self,title):
		self._title = title
		if title is not None and title not in self.sons:
			self.sons.append(title)
		self.sons = list(filter(self.iskey,self.sons))
		self.relayout()
	title = property(lambda self:self._title, set_title)
	def set_doc(self,doc):
		self._doc = doc
		if doc is not None and doc not in self.sons:
			self.sons.append(doc)
		self.sons = list(filter(self.iskey,self.sons))
		self.relayout()
	doc = property(lambda self:self._doc, set_doc)

def MessageBox_defaultlayout_gen(BUTTON_HEIGHT = 30, BUTTON_BLANKING = 10, PADDING = 20, TITLE_PADDING = 20, TITLE_HEIGHT = 30, BUTTON_X = (0.2,20), BUTTON_WIDTH = (0.6,-40)):
	def f(self):
		if self.title is not None:
			self.title.pos = Posattr((0.5,0),(1,-TITLE_PADDING-TITLE_HEIGHT/2),(0,0),(0,0))
		cur_h = PADDING
		if self.buttons is not None:
			for i in range(len(self.buttons)):
				self.buttons[i].pos = Posattr(BUTTON_X,(0,cur_h),BUTTON_WIDTH,(0,BUTTON_HEIGHT))
				cur_h += BUTTON_HEIGHT + BUTTON_BLANKING
		if self.doc is not None:
			self.doc.pos = Posattr((0,PADDING),(0,cur_h),(1,-2*PADDING),(1,-cur_h-TITLE_PADDING-TITLE_HEIGHT))
	return f
MessageBox_defaultlayout = MessageBox_defaultlayout_gen()
	
# 提示选择框（含交互）
class MessageBox(MessageInteractor, LayoutFrame):
	def __init__(self, control, back = None, front = None, title = None,  doc = None, buttons = None, layouter = MessageBox_defaultlayout):
		super(MessageBox, self).__init__(control, back, front)
		self._layouter = layouter
		self._title = None
		self._doc = None
		self._buttons = None
		self.title = title
		self.doc = doc
		self.buttons = buttons if buttons is not None else []
		self.on_resize()
		self.result = 0
	# 注意：请不要多次设置buttons，否则可能导致on_submit事件触发多次
	iskey = lambda self, x: x is self.title or x is self.doc or x in self.buttons
	def set_buttons(self, buttons):
		self._buttons = buttons
		for button in buttons:
			if button not in self.sons:
				self.sons.append(button)
		self.sons = list(filter(self.iskey,self.sons))
		def f(event, id):
			def g():
				self.result = id
				self.dispatch_event('on_submit', self.result)
			return g
		if buttons is not None:
			for i in range(len(buttons)):
				buttons[i].on_press = f(buttons[i].on_press, i)
		self.relayout()
	buttons = property(lambda self:self._buttons, set_buttons)
	def set_text(self,x):
		if self.doc is not None:
			self.doc.text = x
	text = property(lambda self:self.doc.text if self.doc is not None else None,set_text)
	def set_title_text(self,x):
		if self.title is not None:
			self.title.text = x
	title_text = property(lambda self:self.title.text if self.title is not None else None,set_title_text)
	def set_title(self,title):
		self._title = title
		if title is not None and title not in self.sons:
			self.sons.append(title)
		self.sons = list(filter(self.iskey,self.sons))
		self.relayout()
	title = property(lambda self:self._title, set_title)
	def set_doc(self,doc):
		self._doc = doc
		if doc is not None and doc not in self.sons:
			self.sons.append(doc)
		self.sons = list(filter(self.iskey,self.sons))
		self.relayout()
	doc = property(lambda self:self._doc, set_doc)
	def on_submit(self, result):
		# print(result)
		self.hide()

# 提示输入框（含交互）
class MessageInput(AlertBox):
	_TIED_KEY_VAR = '_tied_MessageInput_event_'
	# editable
	def set_submit_key_event(self, event):
		obj, eventname = event
		# print('set_submit_key_event')
		if not getattr(obj, self._TIED_KEY_VAR + eventname, False):
			setattr(obj, self._TIED_KEY_VAR + eventname, True)
			def f(event):
				def g(*args, **kw):
					self.dispatch_event('on_submit', self.text)
					# print('on_submit_')
					return event(*args, **kw)
				return g
			setattr(obj, eventname ,f(getattr(obj, eventname)))
		self._submit_key = getattr(obj, eventname)
	def on_submit(self, text):
		# print('on_submit:%s' % text)
		self.hide()
	submit_key = property(lambda self:self._submit_key,set_submit_key_event)

# def MessagePage_defaultlayout_gen(self):
	# return MessageBox_defaultlayout(self)
	# # 待填

def TagPages_defaultlayoutV_gen(TAG_WIDTH = 90,	TAG_PADDING = 5, TAG_HEIGHT = None, FULL_PAGE = False):
	def TagPages_defaultlayoutV(self):
		if TAG_HEIGHT is None:
			tag_c = -TAG_PADDING*(len(self.pages)+1)/max(1,len(self.pages))
			tag_k = 1/max(1,len(self.pages))
			cur_k = 0
			cur_h = TAG_PADDING
		else:
			tag_c = TAG_HEIGHT
			tag_k = 0
			cur_k = 1
			cur_h = -len(self.pages)*(TAG_HEIGHT+TAG_PADDING)
		for i in range(len(self.pages)-1,-1,-1):
			self.pages[i][0].pos = Posattr((0,0),(cur_k,cur_h),(0,TAG_WIDTH),(tag_k,tag_c))
			cur_k += tag_k
			cur_h += tag_c + TAG_PADDING
			self.pages[i][1].pos = Posattr() if FULL_PAGE else Posattr((0,TAG_WIDTH),(0,0),(1,-TAG_WIDTH),(1,0))
	return TagPages_defaultlayoutV
TagPages_defaultlayoutV = TagPages_defaultlayoutV_gen()

def TagPages_defaultlayoutH_gen(TAG_HEIGHT = 30, TAG_PADDING = 5, TAG_WIDTH = None, FULL_PAGE = False):
	def TagPages_defaultlayoutH(self):
		if TAG_WIDTH is None:
			tag_c = -TAG_PADDING*(len(self.pages)+1)/max(1,len(self.pages))
			tag_k = 1/max(1,len(self.pages))
			cur_k = 0
			cur_w = TAG_PADDING
		else:
			tag_c = TAG_WIDTH
			tag_k = 0
			cur_k = 0
			cur_w = TAG_PADDING
		for i in range(len(self.pages)):
			self.pages[i][0].pos = Posattr((cur_k,cur_w),(1,-TAG_HEIGHT),(tag_k,-tag_c),(0,TAG_HEIGHT))
			cur_k += tag_k
			cur_w += tag_c + TAG_PADDING
			self.pages[i][1].pos = Posattr() if FULL_PAGE else Posattr((0,0),(0,0),(1,0),(1,-TAG_HEIGHT))
	return TagPages_defaultlayoutH
TagPages_defaultlayoutH = TagPages_defaultlayoutH_gen()
			
# 带标签的页面
class TagPages(LayoutFrame):
	def __init__(self, control, pages = None, layouter = TagPages_defaultlayoutV):
		super(TagPages, self).__init__(control)
		self._layouter = layouter
		self.pages = pages if pages is not None else []
	def set_pages(self, pages):
		# print('set_buttons')
		self._pages = pages
		self.sons = []
		for i in range(len(pages)):
			def g(i):
				def f():
					self.page = i
				return f
			pages[i][0].on_press = g(i)
			self.sons += pages[i]
		self.relayout()
		self.page = 0
	pages = property(lambda self:self._pages,set_pages)
	def set_page(self, page):
		self._page = page
		for i in range(len(self.pages)):
			if i == page:
				self.pages[i][0].stage = 1
				if self.visible:
					self.pages[i][1].show()
			else:
				self.pages[i][0].stage = 0
				self.pages[i][1].hide()
		self.dispatch_event('on_switch',self.page)
	page = property(lambda self:self._page,set_page)
	def show(self):
		super(TagPages, self).show()
		for i in range(len(self.pages)):
			if i != self.page:
				self.pages[i][1].hide()
	def on_switch(self, page):
		# print('on switch:%d' % page)
		pass
	def draw(self, range = None):
		if range is None:
			x, y, width, height = self.x, self.y, self.width, self.height
		else:
			x, y, width, height = range
			x = max(x, self.x)
			y = max(y, self.y)
			width = min(width, self.x + self.width - x)
			height = min(height, self.y + self.height - y)
		for i in self.pages:
			if i[1].visible and i[1].intersect(x,y,width,height):
				i[1].draw((x,y,width,height))
		for i in self.pages:
			if i[0].visible and i[0].intersect(x,y,width,height):
				i[0].draw((x,y,width,height))
	def on_mouse_press(self, x, y, button, modifiers):
		flag = False
		for j in range(len(self.pages)-1,-1,-1):
			i = self.pages[j]
			if i[0].visible and i[0].hit_test(x,y):
				i[0].on_mouse_press(x, y, button, modifiers)
				flag = True
				break
		if not flag:
			for j in range(len(self.pages)-1,-1,-1):
				i = self.pages[j]
				if i[1].visible and i[1].hit_test(x,y):
					i[1].on_mouse_press(x, y, button, modifiers)
					flag = True
					break
TagPages.register_event_type('on_switch')

# 科技树
# 也许不应该放在这里 ……
# class TechTree(Frame):
	# class TechTreeNode(object):
		# pass
	# pass

class Form(pyglet.window.Window):
	def __init__(self, width=None, height=None, caption=None, resizable=False, style=None, fullscreen=False, visible=True, vsync=True, display=None, screen=None, config=None, context=None, mode=None):
		super(Form, self).__init__(width, height, caption, resizable, style, fullscreen, visible, vsync, display, screen, config, context, mode)
		
		self.root_control = Frame((self,Posattr(),0,0,width,height))
		# self.root_control.capture_events()
	def on_draw(self):
		pyglet.gl.glClearColor(1, 1, 1, 1)
		pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
		self.clear()
		self.root_control.draw((0,0,self.width,self.height))
	def on_mouse_press(self, x, y, symbol, modifiers):
		# 按下鼠标时清除所有控件句柄
		self.remove_handlers()
		# print('removed handlers')
		self.root_control.on_mouse_press(x, y, symbol, modifiers)
	def on_mouse_motion(self, x, y, dx, dy):
		self.root_control.on_mouse_motion(x, y, dx, dy)
	def draw(self):
		self.clear()
		self.root_control.draw((0,0,self.width,self.height))
	def show(self):
		self.root_control.show()
	def hide(self):
		self.root_control.hide()