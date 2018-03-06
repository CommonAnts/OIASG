#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import pyglet
from lib import *

pyglet.clock.set_fps_limit(60)

pyglet.resource.path = ['resource']

window = controls.Form(200,100)
root = window.root_control

# mv = pyglet.resource.media('tmp4.mp4', streaming=False)
# mv.play()

root.sons = [
	controls.Button((window,25,15,150,30,root),pyglet.text.Label('按钮测试',font_name='微软雅黑',font_size=16,anchor_x = 'center',anchor_y = 'center')
	,pyglet.sprite.Sprite(pyglet.resource.image('tbut.png'))
	,pyglet.sprite.Sprite(pyglet.resource.image('tico.png'))
	,pyglet.sprite.Sprite(pyglet.resource.image('t.png'))
	),
	controls.Button((window,25,55,150,30,root),pyglet.text.Label('按钮测试',font_size=16,bold = True,anchor_x = 'center',anchor_y = 'center')
	,pyglet.sprite.Sprite(pyglet.resource.image('tbut.png'))
	,pyglet.sprite.Sprite(pyglet.resource.image('tico.png')))
]
button0,button1 = root.sons

def onp():
	print('pressed button 0')
	if button1.visible:
		button1.hide()
	else:
		button1.show()

def onp1():
	print('pressed button 1')
button0.on_press = onp
button1.on_press = onp1

@window.event
def on_mouse_press(x, y, symbol, modifiers):
	root.on_mouse_press(x, y, symbol, modifiers)

window.show()
pyglet.app.run()