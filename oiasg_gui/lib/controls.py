#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pyglet

# 控件
class Control(pyglet.event.EventDispatcher):
	# x,y:控件位置
	# width,height:控件大小
	# visible:是否在显示
	visible = False
	sons = []
	def __init__(self, window = None, x = 0, y = 0, width = 0, height = 0, parent = None):
		super(Control, self).__init__()
		# parent:控件的上级
		self.window = window
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.parent = parent
	# 碰撞检测：坐标是否在控件的矩形区域之内（严格）
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

# 按钮
class Button(Control):
	# image:背景图片(Sprite类型)
	# icon:(左侧)图标(Sprite类型)
	# pressed_image:按下时的背景图片(Sprite类型)
	# label:文字(Lable/HTMLLable类型)
	# text:文字值
	# charged:是否被按下
	charged = False
	def __init__(self, control, label = None, image = None, icon = None, pressed_image = None):
		super(Button, self).__init__(*control)
		self.label = label
		self.image = image
		self.icon = icon
		self.pressed_image = pressed_image
		self.resize()
		self.text = property(lambda self:self.label.text,self.set_text)
	def resize(self):
		if self.image is not None:
			self.image.update(x = self.x, y = self.y, scale_x = self.width / self.image.width , scale_y = self.height / self.image.height)
		if self.pressed_image is not None:
			self.pressed_image.update(x = self.x, y = self.y, scale_x = self.width / self.pressed_image.width , scale_y = self.height / self.pressed_image.height)
		if self.icon is not None:
			self.icon.update(x = self.x, y = self.y, scale = self.height / self.icon.height)
	def set_text(self,x):
		self.label.text = x
	def draw_text(self):
		if self.label is not None:
			self.label.x = self.x + self.width / 2
			self.label.y = self.y + self.height / 2
			self.label.draw()
	def draw_image(self):
		if self.charged:
			if self.pressed_image is not None:
				self.pressed_image.update(x = self.x, y = self.y)
				self.pressed_image.draw()
			elif self.image is not None:
				self.image.color = (216,204,192)
				self.image.update(x = self.x, y = self.y)
				self.image.draw()
		else:
			if self.image is not None:
				self.image.color = (255,255,255)
				self.image.update(x = self.x, y = self.y)
				self.image.draw()
	def draw_icon(self):
		if self.icon is not None:
			self.icon.color = ((216,204,192) if self.charged else (255,255,255))
			self.icon.update(x = self.x, y = self.y)
			self.icon.draw()
	def draw(self):
		super(Button, self).draw()
		self.draw_image()
		self.draw_text()
		self.draw_icon()
	def on_mouse_press(self, x, y, button, modifiers):
		print('got mouse press')
		super(Button, self).on_mouse_press(x, y, button, modifiers)
		self.capture_events()
		self.charged = True
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		print('got mouse drag')
		self.charged = self.hit_test(x, y)
	def on_mouse_release(self, x, y, button, modifiers):
		print('got mouse release')
		self.release_events()
		if self.hit_test(x, y):
			self.dispatch_event('on_press')
		self.charged = False
# on_press:从按钮松开时触发事件
Button.register_event_type('on_press')

# 精灵（用于控件）
class Sprite(pyglet.sprite.Sprite):
	def show(self):
		self.visible = True
	def hide(self):
		self.visible = False

# 文本框
class TextBox(Control):
	pass

# 横向进度条
class HBar(Control):
	pass

# 视口覆盖器
# 注意！它渲染时会覆盖页面其余部分，请仅使用一次
# 请务必在任何时刻把含有覆盖器的控件放在其父亲sons[]的首位
class Viewport(Control):
	pass

# 框架（控件组容器）
class Frame(Control):
	pass

# 按钮条
class ButtonSlider(Frame):
	pass

# 按钮菜单
class ButtonMenu(Frame):
	pass

# （屏幕中间）提示选择框
class MessageBox(Frame):
	pass

# （屏幕中间）提示输入框
class MessageInput(Frame):
	pass


# 事件页面
class MessagePage(Frame):
	pass

# 科技树
class TechTree(Frame):
	class TechTreeNode(object):
		pass
	pass

# 带标签的页面
class TagPages(Frame):
	pass

class Form(pyglet.window.Window):
	def __init__(self, width=None, height=None, caption=None, resizable=False, style=None, fullscreen=False, visible=True, vsync=True, display=None, screen=None, config=None, context=None, mode=None):
		super(Form, self).__init__(width, height, caption, resizable, style, fullscreen, visible, vsync, display, screen, config, context, mode)
		
		self.root_control = Control(self,0,0,width,height)
		self.root_control.capture_events()
	def on_draw(self):
		self.clear()
		self.root_control.draw()
	# 奇怪的是这个函数会导致按钮无法隐藏，而修改实例却无此问题
	# def on_mouse_press(self, x, y, symbol, modifiers):
		# self.root_control.on_mouse_press(x, y, symbol, modifiers)
	def draw(self):
		self.clear()
		self.root_control.draw()
	def show(self):
		self.root_control.show()
	def hide(self):
		self.root_control.hide()