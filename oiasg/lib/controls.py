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
			return int(width*p[0]+p[1])
		def c_v(p):
			return int(height*p[0]+p[1])
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
	def __init__(self, window = None, parent = None, pos = Posattr(), x = 0, y = 0, width = 1, height = 1):
		super(Control, self).__init__()
		# parent:控件的上级
		self.visible = False
		self.sons = []
		self.window = window
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.parent = parent
		self.pos = pos
	# 碰撞检测：坐标是否在控件的矩形区域之内（严格）
	def on_resize(self):
		pass
	def hit_test(self, x, y):
		return (self.x < x < self.x + self.width and
				self.y < y < self.y + self.height)
	def intersect(self,x,y,width,height):
		if x > self.x+self.width or self.x > x + width or y > self.y+height or self.y > y+height:
			return False
		return True
	# 显示和隐藏
	def show(self):
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
	def draw(self):
		for i in self.sons:
			if i.visible and i.intersect(self.x,self.y,self.width,self.height):
				i.draw()
	def on_mouse_press(self, x, y, button, modifiers):
		for i in self.sons:
			if i.visible and i.hit_test(x,y):
				i.on_mouse_press(x, y, button, modifiers)
	# 事件处理句柄：在点击激活控件后跟踪后续事件
	def capture_events(self):
		if self.window is not None:
			self.window.push_handlers(self)
	def release_events(self):
		if self.window is not None:
			self.window.remove_handlers(self)
Control.register_event_type('on_mouse_press')

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
		super(Label, self).on_resize()
		if self.label is not None:
			self.label.x = self.x + self.width / 2
			self.label.y = self.y + self.height / 2
	def draw(self):
		super(Label, self).draw()
		self._draw(self.label)

# 精灵控件
class SpriteControl(Control):
	def __init__(self, control, image = None):
		super(SpriteControl, self).__init__(*control)
		self.image = image
		self.on_resize()
	def on_resize(self):
		super(SpriteControl, self).on_resize()
		if self.image is not None:
			self.image.update(x = self.x, y = self.y, scale_x = self.width / self.image.t_width , scale_y = self.height / self.image.t_height)
	def draw(self):
		super(SpriteControl, self).draw()
		self._draw(self.image)

class Button(Control):
	# image:背景图片(Sprite类型)
	# icon:(左侧)图标(Sprite类型)
	# pressed_image:按下时的背景图片(Sprite类型)
	# label:文字(Lable/HTMLLable类型)
	# text:文字值
	# charged:是否被按下
	# direction:方向{0:图标靠左,1:图标靠右,2:图标靠上,3:图标靠下}
	
	# 按钮于按下到松开之间获取事件控制句柄
	charged = False
	def __init__(self, control, label = None, image = None, icon = None, pressed_image = None, direction = 0):
		super(Button, self).__init__(*control)
		self.label = label
		self.image = image
		self.icon = icon
		self.pressed_image = pressed_image
		self.direction = direction
		self.on_resize()
	def set_text(self, x):
		self.label.text = x
	text = property(lambda self:self.label.text,set_text)
	def on_resize(self):
		super(Button, self).on_resize()
		if self.image is not None:
			self.image.update(x = self.x, y = self.y, scale_x = self.width / self.image.t_width , scale_y = self.height / self.image.t_height)
		if self.pressed_image is not None:
			self.pressed_image.update(x = self.x, y = self.y, scale_x = self.width / self.pressed_image.t_width , scale_y = self.height / self.pressed_image.t_height)
		if self.icon is not None:
			if self.direction == 0:
				k = self.height / self.icon.t_height
				self.icon.update(x = self.x, y = self.y, scale = k)
			elif self.direction == 1:
				k = self.height / self.icon.t_height
				self.icon.update(x = self.x+self.width-k*self.icon.t_width, y = self.y, scale = k)
			elif self.direction == 2:
				k = self.width / self.icon.t_width
				self.icon.update(x = self.x, y = self.y+self.height-k*self.icon.t_height, scale = k)
			elif self.direction == 3:
				k = self.width / self.icon.t_width
				self.icon.update(x = self.x, y = self.y, scale = k)
		if self.label is not None:
			self.label.x = self.x + self.width / 2
			self.label.y = self.y + self.height / 2
	def draw_image(self):
		if self.charged:
			if self.pressed_image is not None:
				self.pressed_image.draw()
			elif self.image is not None:
				# self.image.color = (216,204,192)
				self.image.draw()
		else:
			if self.image is not None:
				# self.image.color = (255,255,255)
				self.image.draw()
	def draw(self):
		# print('drawn a button')
		super(Button, self).draw()
		self.draw_image()
		self._draw(self.label)
		self._draw(self.icon)
	def on_mouse_press(self, x, y, button, modifiers):
		# print('got mouse press')
		super(Button, self).on_mouse_press(x, y, button, modifiers)
		self.capture_events()
		self.dispatch_event('on_click')
		self.charged = True
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		# print('got mouse drag')
		self.charged = self.hit_test(x, y)
	def on_mouse_release(self, x, y, button, modifiers):
		# print('got mouse release')
		self.release_events()
		if self.hit_test(x, y):
			self.dispatch_event('on_press')
		self.charged = False
	def on_press(self):
		pass
# on_press:从按钮松开时触发事件
Button.register_event_type('on_click')
Button.register_event_type('on_press')

# 多外观按钮
class SwitchButton(Button):
	def __init__(self, control, labels = None, images = None, icons = None, pressed_images = None, direction = 0):
		super(SwitchButton, self).__init__(control)
		self.labels = labels
		self.images = images
		self.icons = icons
		self.pressed_images = pressed_images
		self.direction = direction
		self.stage = 0		
	def _get(self, x, id):
		if x is None:
			return None
		elif len(x) > id:
			return x[id]
		else:
			return None
	def set_stage(self, _stage):
		self._stage = _stage
		self.label = self._get(self.labels,self.stage)
		self.image = self._get(self.images,self.stage)
		self.icon = self._get(self.icons,self.stage)
		self.pressed_image = self._get(self.pressed_images,self.stage)
		self.on_resize()
	stage = property(lambda self:self._stage,set_stage)

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
	def __init__(self, control, text = None, style = None, editable = False, multiline = False, back = None, padding = 0, select_backcolor = None, select_textcolor = None, caret_color = None):
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
		super(TextBox, self).on_resize()
		if self.back is not None:
			self.back.update(x = self.x, y = self.y, scale_x = self.width / self.back.t_width , scale_y = self.height / self.back.t_height)
		if self.layout is not None:
			self.layout.x = self.x + self.padding
			self.layout.y = self.y + self.padding
			self.layout.width = self.width-self.padding*2
			self.layout.height = self.height-self.padding*2
	def draw(self):
		super(TextBox, self).draw()
		self._draw(self.back)
		self._draw(self.layout)
	def on_mouse_press(self, x, y, button, modifiers):
		# print('got mouse press')
		super(TextBox, self).on_mouse_press(x, y, button, modifiers)
		if self.window is not None and self.caret is not None:
			self.window.push_handlers(self.caret)

class FormattedTextBox(TextBox):
	def __init__(self, control, doc = None, editable = False, multiline = False, back = None, padding = 0, select_backcolor = None, select_textcolor = None, caret_color = None):
		super(TextBox, self).__init__(*control)
		self.editable = editable
		self.back = back
		self.padding = padding
		self.multiline = multiline
		self.layout = None
		self.doc = doc
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
	doc = property(lambda self:self._doc,set_doc)

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
		super(ProgressBar, self).on_resize()
		if self.back is not None:
			self.back.update(x = self.x, y = self.y, scale_x = self.width / self.back.t_width , scale_y = self.height / self.back.t_height)
		if self.bar is not None:
			K = self.bar_sizerate
			ra = self._rate
			L,R,U,D = self.x + self.width*K[0],self.x + self.width*(K[0]+K[2]),self.y + self.height*(K[1]+K[3]),self.y + self.height*K[1]
			if self.direction == 0:
				self.bar.update(x = L, y = D, scale_x = (R-L)*ra/self.bar.t_width, scale_y = (U-D)/self.bar.t_height)
			elif self.direction == 1:
				self.bar.update(x = R-(R-L)*ra/self.bar.t_width, y = D, scale_x = (R-L)*ra/self.bar.t_width, scale_y = (U-D)/self.bar.t_height)
			elif self.direction == 2:
				self.bar.update(x = L, y = D, scale_x = (R-L)/self.bar.t_width, scale_y = (U-D)*ra/self.bar.t_height)
			elif self.direction == 3:
				self.bar.update(x = L, y = U-(U-D)*ra/self.height, scale_x = (R-L)/self.bar.t_width, scale_y = (U-D)*ra/self.bar.t_height)
		if self.label is not None:
			self.label.x = self.x + self.width / 2
			self.label.y = self.y + self.height / 2
	def set_text(self,x):
		self.label.text = x
	text = property(lambda self:self.label.text,set_text)
	def draw(self):
		super(ProgressBar, self).draw()
		self._draw(self.back)
		self._draw(self.bar)
		self._draw(self.label)

# 水平滚动条	
class Slider(Control):
	# image:背景图片(Sprite类型)
	# cursor:游标(Sprite类型)
	
	# 游标于按下到松开之间获取事件控制句柄
	def __init__(self, control, image = None, cursor = None, rate = 1):
		super(Slider, self).__init__(*control)
		self.image = image
		self.cursor = cursor
		self.rate = rate
	def set_rate(self, x):
		x = max(0,min(x,1))
		self._rate = x
		self.on_resize()
	rate = property(lambda self:self._rate,set_rate)
	def on_resize(self):
		super(Slider, self).on_resize()
		if self.image is not None:
			self.image.update(x = self.x, y = self.y + self.height/2 - self.image.t_height/2, scale_x = self.width / self.image.t_width)
		if self.cursor is not None:
			k = self.height / self.cursor.t_height
			self.cursor.update(x = self.x + self.rate*(self.width - k * self.cursor.t_width), y = self.y, scale = k)
	def draw(self):
		super(Slider, self).draw()
		self._draw(self.image)
		self._draw(self.cursor)
	def on_mouse_press(self, x, y, button, modifiers):
		# print('got mouse press')
		super(Slider, self).on_mouse_press(x, y, button, modifiers)
		self.rate = (x-self.x-self.cursor.width/2)/max(1,self.width-self.cursor.width)
		self.capture_events()
		self.dispatch_event('on_begin_scroll')
		self.dispatch_event('on_change', self.rate)
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.rate = (x-self.x-self.cursor.width/2)/max(1,self.width-self.cursor.width)
		self.dispatch_event('on_change', self.rate)
	def on_mouse_release(self, x, y, button, modifiers):
		self.release_events()
		self.dispatch_event('on_end_scroll')
	def on_change(self,val):
		# print(val)
		pass

Slider.register_event_type('on_begin_scroll')
Slider.register_event_type('on_end_scroll')
Slider.register_event_type('on_change')
	
# 垂直滚动条
class ScrollBar(Slider):
	def on_resize(self):
		super(Slider, self).on_resize()
		if self.image is not None:
			self.image.update(x = self.x + self.width/2 - self.image.t_width/2, y = self.y, scale_y = self.height / self.image.t_height)
		if self.cursor is not None:
			k = self.width / self.cursor.t_width
			self.cursor.update(x = self.x, y = self.y + (1-self.rate)*(self.height - k * self.cursor.t_height), scale = k)
	def on_mouse_press(self, x, y, button, modifiers):
		# print('got mouse press')
		super(Slider, self).on_mouse_press(x, y, button, modifiers)
		self.rate = 1-(y-self.y-self.cursor.height/2)/max(1,self.height-self.cursor.height)
		self.capture_events()
		self.dispatch_event('on_begin_scroll')
		self.dispatch_event('on_change', self.rate)
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.rate = 1-(y-self.y-self.cursor.height/2)/max(1,self.height-self.cursor.height)
		self.dispatch_event('on_change', self.rate)

# 框架（控件组及布局容器）
class Frame(Control):
	def __init__(self, control):
		super(Frame, self).__init__(*control)
		self.on_resize()
	def on_resize(self):
		# print(self.x,self.y,self.height,self.width)
		super(Frame, self).on_resize()
		for i in self.sons:
			i.x , i.y , i.width ,i.height = i.pos(self.x,self.y,self.width,self.height)
			i.on_resize()

# 视口
class Viewport(Frame):
	def draw(self):
		t = pyglet.image.get_buffer_manager().get_color_buffer().get_texture()
		super(Viewport, self).draw()
		f = pyglet.image.get_buffer_manager().get_color_buffer().get_region(self.x,self.y,self.width,self.height).get_texture()
		t.blit(0,0)
		f.blit(self.x,self.y)

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

# 图片框架
class ImageFrame(Frame):
	# back:背景图片(AbstractImage)
	# front:前景图片(AbstractImage)
	def __init__(self, control, back = None, front = None):
		self.back = back
		self.front = front
		super(ImageFrame, self).__init__(control)
	def draw(self):
		self._draw(self.back)
		super(ImageFrame, self).draw()
		self._draw(self.front)
	def on_resize(self):
		super(ImageFrame, self).on_resize()
		if self.back is not None:
			self.back.update(x = self.x, y = self.y, scale_x = self.width / self.back.t_width , scale_y = self.height / self.back.t_height)
		if self.front is not None:
			self.front.update(x = self.x, y = self.y, scale_x = self.width / self.front.t_width , scale_y = self.height / self.front.t_height)

class ImageLayoutFrame(ImageFrame,LayoutFrame):
	def __init__(self, control, back = None, front = None, layouter = lambda self:None):
		super(ImageLayoutFrame, self).__init__(control,back,front)
		self.layouter = layouter
			
def ScrollTextBox_defaultlayout(self):
	SCROLL_BAR_WIDTH = 20
	if self.scrollbar is not None:
		self.scrollbar.pos = Posattr((1,-SCROLL_BAR_WIDTH),(0,0),(0,SCROLL_BAR_WIDTH),(1,0))
	if self.doc is not None:
		self.doc.pos = Posattr((0,0),(0,0),(1,-SCROLL_BAR_WIDTH),(1,0))
class ScrollTextBox(LayoutFrame):
	def __init__(self, control, doc = None, scrollbar = None, layouter = ScrollTextBox_defaultlayout):
		super(ScrollTextBox, self).__init__(control)
		self._layouter = layouter
		self._doc = doc
		self._scrollbar = scrollbar
		self.doc = doc
		self.scrollbar = scrollbar
		self.layouter = layouter
		self.on_resize()
	iskey = lambda self, x: x is self.scrollbar or x is self.doc
	def set_text(self,x):
		if self.doc is not None:
			self.doc.text = x
	text = property(lambda self:self.doc.text if self.doc is not None else None,set_text)
	def set_doc(self,doc):
		self._doc = doc
		if doc is not None and doc not in self.sons:
			self.sons.append(doc)
		self.sons = list(filter(self.iskey,self.sons))
		self.relayout()
	doc = property(lambda self:self._doc, set_doc)
	def set_scrollbar(self,scrollbar):
		self._scrollbar = scrollbar
		if scrollbar is not None:
			if scrollbar not in self.sons:
				self.sons.append(scrollbar)
			if self.doc is not None and self.doc.layout is not None:
				def f(event):
					def g(*args, **kw):
						self.doc.layout.ensure_line_visible(min(max(int(args[0]*self.doc.layout.get_line_count()),0),self.doc.layout.get_line_count()-1))
						return event(*args, **kw)
					return g
				self.scrollbar.on_change = f(self.scrollbar.on_change)
		self.sons = list(filter(self.iskey,self.sons))
		self.relayout()
	scrollbar = property(lambda self:self._scrollbar,set_scrollbar)

def ButtonSlider_defaultlayout(self):
	PADDING_RATE = 0.2
	HPADDING_RATE = 0.5
	VPADDING_RATE = 0.15
	rate = 1/(len(self.sons)*(1+PADDING_RATE)-PADDING_RATE+2*HPADDING_RATE)
	padding_rate = PADDING_RATE * rate
	hpadding_rate = HPADDING_RATE * rate
	cur_t = hpadding_rate
	for i in self.sons:
		i.pos = Posattr((cur_t,0),(VPADDING_RATE,0),(rate,0),(1-VPADDING_RATE*2,0))
		cur_t += rate + padding_rate
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
			self.sons[i].on_press = g(i+1)
		self.relayout()
	buttons = property(lambda self:self.sons,set_buttons)
	def set_val(self, v):
		self._val = v
		for i in range(min(v,len(self.sons))):
			self.sons[i].stage = 0
		for i in range(v,len(self.sons)):
			self.sons[i].stage = 1
		self.dispatch_event('on_change',self._val)
	val = property(lambda self:self._val,set_val)
	def on_change(self, val):
		pass
ButtonSlider.register_event_type('on_change')

# 交互式事件窗口
class MessageInteractor(ImageFrame):
	def set_submit_key_event(self, event):
		obj, eventname = event
		# print('set_submit_key_event')
		def f(event):
			def g(*args, **kw):
				self.dispatch_event('on_submit')
				# print('on_submit_')
				return event(*args, **kw)
			return g
		setattr(obj, eventname ,f(getattr(obj, eventname)))
		self._submit_key = getattr(obj, eventname)
	def on_submit(self):
		# print('on_submit')
		self.hide()
	submit_key = property(lambda self:self._submit_key,set_submit_key_event)
MessageInteractor.register_event_type('on_submit')

def AlertBox_defaultlayout(self):
	BUTTON_HEIGHT = 30
	BUTTON_BLANKING = 10
	PADDING = 20
	TITLE_PADDING = 20
	TITLE_HEIGHT = 30
	if self.title is not None:
		self.title.pos = Posattr((0.5,0),(1,-TITLE_PADDING-TITLE_HEIGHT/2),(0,0),(0,0))
	cur_h = PADDING
	if self.button is not None:
		self.button.pos = Posattr((0.2,PADDING),(0,cur_h),(0.6,-2*PADDING),(0,BUTTON_HEIGHT))
	cur_h += BUTTON_HEIGHT + BUTTON_BLANKING
	if self.doc is not None:
		self.doc.pos = Posattr((0,PADDING),(0,cur_h),(1,-2*PADDING),(1,-cur_h-TITLE_PADDING-TITLE_HEIGHT))
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

def MessageBox_defaultlayout(self):
	BUTTON_HEIGHT = 30
	BUTTON_BLANKING = 10
	PADDING = 20
	TITLE_PADDING = 20
	TITLE_HEIGHT = 30
	if self.title is not None:
		self.title.pos = Posattr((0.5,0),(1,-TITLE_PADDING-TITLE_HEIGHT/2),(0,0),(0,0))
	cur_h = PADDING
	if self.buttons is not None:
		for i in range(len(self.buttons)):
			self.buttons[i].pos = Posattr((0.2,PADDING),(0,cur_h),(0.6,-2*PADDING),(0,BUTTON_HEIGHT))
			cur_h += BUTTON_HEIGHT + BUTTON_BLANKING
	if self.doc is not None:
		self.doc.pos = Posattr((0,PADDING),(0,cur_h),(1,-2*PADDING),(1,-cur_h-TITLE_PADDING-TITLE_HEIGHT))
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
			def g(*args, **kw):
				self.result = id
				self.dispatch_event('on_submit', self.result)
				return event(*args, **kw)
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
	# editable
	def set_submit_key_event(self, event):
		obj, eventname = event
		# print('set_submit_key_event')
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

def MessagePage_defaultlayout(self):
	return MessageBox_defaultlayout(self)
	# 待填

# 事件页面
# 布局待设计 ……
class MessagePage(MessageBox):
	def __init__(self, control, back = None, front = None, title = Label(()),  doc = TextBox((),'',{}), buttons = None, layouter = MessagePage_defaultlayout):
		super(MessagePage, self).__init__(control, back, front, title, doc, buttons, layouter)

def TagPages_defaultlayoutV(self):
	TAG_WIDTH = 90
	TAG_PADDING = 5
	tag_c = TAG_PADDING*(len(self.pages)+1)/max(1,len(self.pages))
	tag_k = 1/max(1,len(self.pages))
	cur_k = 0
	cur_h = TAG_PADDING
	for i in range(len(self.pages)):
		self.pages[i][0].pos = Posattr((0,0),(cur_k,cur_h),(0,TAG_WIDTH),(tag_k,-tag_c))
		cur_k += tag_k
		cur_h += - tag_c + TAG_PADDING
		self.pages[i][1].pos = Posattr((0,TAG_WIDTH),(0,0),(1,-TAG_WIDTH),(1,0))

def TagPages_defaultlayoutH(self):
	TAG_HEIGHT = 30
	TAG_PADDING = 5
	tag_c = TAG_PADDING*(len(self.pages)+1)/max(1,len(self.pages))
	tag_k = 1/max(1,len(self.pages))
	cur_k = 0
	cur_w = TAG_PADDING
	for i in range(len(self.pages)):
		self.pages[i][0].pos = Posattr((cur_k,cur_w),(1,-TAG_HEIGHT),(tag_k,-tag_c),(0,TAG_HEIGHT))
		cur_k += tag_k
		cur_w += - tag_c + TAG_PADDING
		self.pages[i][1].pos = Posattr((0,0),(0,0),(1,0),(1,-TAG_HEIGHT))

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
		
		self.root_control = Frame((self,None,Posattr(),0,0,width,height))
		# self.root_control.capture_events()
	def on_draw(self):
		pyglet.gl.glClearColor(1, 1, 1, 1)
		pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
		self.clear()
		self.root_control.draw()
	def on_mouse_press(self, x, y, symbol, modifiers):
		# 按下鼠标时清除所有控件句柄
		self.remove_handlers()
		# print('removed handlers')
		self.root_control.on_mouse_press(x, y, symbol, modifiers)
	def draw(self):
		self.clear()
		self.root_control.draw()
	def show(self):
		self.root_control.show()
	def hide(self):
		self.root_control.hide()