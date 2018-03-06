#!/usr/bin/python
# -*- coding: UTF-8 -*-

import random
import time

import pyglet
from lib import *

pyglet.clock.set_fps_limit(60)

pyglet.resource.path = ['resource']

window = controls.Form(800,600,resizable = True)
root = window.root_control

@window.event
def on_resize(width, height):
	root.width = width
	root.height = height
	root.on_resize()
# mv = pyglet.resource.media('tmp4.mp4', streaming=False)
# mv.play()

root.sons = [
	controls.Viewport((window,0,0,800,600,root),
	controls.Sprite(pyglet.resource.image('tbut.png')),
	(0.05,0.05,0.9,0.9))
	,
	controls.Button((window,25,15,150,30,root,controls.Posattr((0,25),(0,15),(0,150),(0,30))),pyglet.text.Label('隐藏其它',font_name='微软雅黑',font_size=16,anchor_x = 'center',anchor_y = 'center')
	,controls.Sprite(pyglet.resource.image('tbut.png'))
	,controls.Sprite(pyglet.resource.image('tico.png'))
	,controls.Sprite(pyglet.resource.image('t.png'))
	)
]
vport,button0 = root.sons
vport.sons = [
	controls.Button((window,25,55,150,30,root,controls.Posattr((0,25),(0,55),(0,150),(0,30))),pyglet.text.Label('+=10%',font_size=16,bold = True,anchor_x = 'center',anchor_y = 'center')
	,controls.Sprite(pyglet.resource.image('tbut.png'))
	,controls.Sprite(pyglet.resource.image('tico.png'))
	),
	controls.TextBox((window,25,100,150,150,root,controls.Posattr((0,25),(0,100),(0,150),(0,150))),'''这是一个多行文本框
qwq''',
	{'color':(0, 0, 200, 255),'font_name':'仿宋','font_size':14,'line_spacing':24,'wrap':'char'},editable = True,
	multiline = True,back = controls.Sprite(pyglet.resource.animation('walk.gif')),select_backcolor = (0, 0, 200, 127)
	)
	,
	controls.ProgressBar((window,25,265,150,20,root,controls.Posattr((0,25),(0,265),(0,150),(0,20))),pyglet.text.Label('%',font_size=14,bold = True,anchor_x = 'center',anchor_y = 'center'), back = controls.Sprite(pyglet.resource.image('tbut.png')), bar = controls.Sprite(pyglet.resource.image('progressh.png')), bar_sizerate = (0.05,0.2,0.9,0.6), direction = 0, rate = 1
	)
]
# for i in range(0,1000):
	# # root.sons = root.sons[:3]
	# while(len(root.sons)>3):
		# del(root.sons[-1])
		# root.sons.pop()
	# for i in range(0,180):
		# root.sons.append(
		# controls.Button((window,random.randint(180,window.width),random.randint(0,window.height),random.randint(0,600),random.randint(0,600),root),
		# pyglet.text.Label('按钮测试',font_size=16,bold = True,anchor_x = 'center',anchor_y = 'center'),
		# image = pyglet.sprite.Sprite(pyglet.resource.image('tbut.png')),
		# icon = pyglet.sprite.Sprite(pyglet.resource.image('tico.png'))))

button1,txtbox1,prog = vport.sons
# button1.label.text = '111'
# print(button1.text)
# button1.text = '11'
def onp():
	print('pressed button 0')
	if button1.visible:
		button1.hide()
	else:
		button1.show()
	if txtbox1.visible:
		txtbox1.hide()
	else:
		txtbox1.show()
	if prog.visible:
		prog.hide()
	else:
		prog.show()
	if vport.visible:
		vport.hide()
	else:
		vport.show()
	

def onp1():
	print('pressed button 1')
	# print(button1.text)
	# button1.text = '11'
	prog.rate = (prog.rate + 0.1 - (prog.rate + 0.1)// 1)
	prog.text = '%.1f%%' % (prog.rate*100)
	
button0.on_press = onp
button1.on_press = onp1

window.show()
pyglet.app.run()