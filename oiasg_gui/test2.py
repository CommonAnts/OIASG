#!/usr/bin/python
# -*- coding: UTF-8 -*-

import random

from .lib import *

import pyglet

fps_display = pyglet.clock.ClockDisplay()

pyglet.resource.path = ['resource']

window = controls.Form(800, 600, resizable=True)
root = window.root_control

bat = pyglet.graphics.Batch()


def on_draw():
	window.clear()
	root.draw()
	fps_display.draw()


window.on_draw = on_draw


@window.event
def on_resize(width, height):
	root.width = width
	root.height = height
	root.on_resize()


# mv = pyglet.resource.media('tmp4.mp4', streaming=False)
# mv.play()

root.sons = [
	controls.ImageFrame(
		(window, 0, 0, 800, 600, root),
		back=controls.Sprite(pyglet.resource.image('tbut.png')),
		front=controls.Sprite(pyglet.resource.image('tframe.png'))
	)
	,
	controls.Button(
		(window, 25, 15, 150, 30, root, controls.Posattr((0, 25), (0, 15), (0, 150), (0, 30))),
		pyglet.text.Label('隐藏其它', font_name='微软雅黑', font_size=16, anchor_x='center', anchor_y='center'),
		controls.Sprite(pyglet.resource.image('tbut.png')),
		controls.Sprite(pyglet.resource.image('tico.png')),
		controls.Sprite(pyglet.resource.image('t.png'))
	)
]
f1, button0 = root.sons
f1.sons = [
	controls.Viewport((window, 0, 0, 1, 1, f1, controls.Posattr((0.1, 0), (0.1, 0), (0.8, 0), (0.8, 0))))
]
vport = f1.sons[0]
gbutton = lambda: controls.Button(
	(window, 25, 15, 150, 30, root,
	 controls.Posattr((0, random.randint(0, 800)), (0, random.randint(0, 600)), (0, 100), (0, 100))),
	pyglet.text.Label('提交', font_name='黑体', font_size=16, anchor_x='center', anchor_y='center')
	,
	controls.Sprite(pyglet.resource.animation('walk.gif'))
	,
	controls.Sprite(pyglet.resource.image('tico.png'))
)
gtitle = lambda: controls.Label(
	[window],
	pyglet.text.Label(
		'TITLE', font_size=16, bold=True, anchor_x='center', anchor_y='center')
)
gtxtbox = lambda: controls.TextBox(
	[window],
	'''这是一个多行文本框
qwq''',
	{'color': (0, 0, 200, 255), 'font_name': '仿宋', 'font_size': 14, 'line_spacing': 24, 'wrap': 'char'},
	editable=False, multiline=True,
	back=controls.Sprite(pyglet.resource.animation('walk.gif')), select_backcolor=(0, 0, 200, 127)
)


def gdoc():
	doc = pyglet.text.document.FormattedDocument('''这是一个可编辑的多行文本框
qwq''')
	doc.set_style(0, len(doc.text) - 4,
	              {'color': (0, 0, 200, 255), 'font_name': '仿宋', 'font_size': 14, 'line_spacing': 24, 'wrap': 'char'})
	return doc


geditbox = lambda: controls.FormattedTextBox(
	[window],
	gdoc(),
	editable=True, multiline=True,
	back=controls.Sprite(pyglet.resource.image('tbut.png')), select_backcolor=(0, 0, 200, 127)
)
gsbutton = lambda: controls.SwitchButton(
	(window, 0, 0, 1, 1, vport, controls.Posattr((0, 25), (0, 300), (0, 150), (0, 30))),
	[
		pyglet.text.Label('switch0', font_size=16, bold=True, anchor_x='center', anchor_y='center'),
		pyglet.text.Label('switch1', font_size=16, color=(0, 255, 0, 255), bold=True, anchor_x='center',
		                  anchor_y='center')
	]
	,
	[
		controls.Sprite(pyglet.resource.image('tbut.png')),
		controls.Sprite(pyglet.resource.image('tbut.png'))
	]
	,
	[
		controls.Sprite(pyglet.resource.image('tico.png'))
	]
	,
	direction=1
)
gscrollbar = lambda: controls.ScrollBar(
	(window, 25, 380, 150, 30, vport, controls.Posattr((0, 25), (0, 380), (0, 20), (0, 120))),
	image=controls.Sprite(pyglet.resource.image('scroll.png')),
	cursor=controls.Sprite(pyglet.resource.image('sliderf1.png'))
)
vport.sons = [
	controls.Button(
		(window, 0, 0, 1, 1, vport, controls.Posattr((0, 25), (0, 55), (0, 150), (0, 30))),
		pyglet.text.Label('+=10%', font_size=16, bold=True, anchor_x='center', anchor_y='center'),
		controls.Sprite(pyglet.resource.image('tbut.png')),
		controls.Sprite(pyglet.resource.image('tico.png'))
	),
	controls.TextBox(
		(window, 0, 0, 1, 1, vport, controls.Posattr((0, 25), (0, 100), (0, 150), (0, 150))),
		'''这是一个多行文本框
qwq''',
		{'color': (0, 0, 200, 255), 'font_name': '仿宋', 'font_size': 14, 'line_spacing': 24, 'wrap': 'char'},
		editable=False, multiline=True,
		back=controls.Sprite(pyglet.resource.image('tbut.png')), select_backcolor=(0, 0, 200, 127)
	)
	,
	controls.ProgressBar(
		(window, 0, 0, 1, 1, vport, controls.Posattr((0, 25), (0, 265), (0, 150), (0, 20))),
		pyglet.text.Label('%', font_size=14, bold=True, anchor_x='center', anchor_y='center'),
		back=controls.Sprite(pyglet.resource.image('tbut.png')),
		bar=controls.Sprite(pyglet.resource.image('progressh.png')), bar_sizerate=(0.05, 0.2, 0.9, 0.6),
		direction=0,
		rate=1
	)
	,
	gsbutton()
	,
	controls.ButtonSlider(
		(window, 25, 340, 150, 30, vport, controls.Posattr((0, 25), (0, 340), (0, 150), (0, 30))),
		back=controls.Sprite(pyglet.resource.image('bslider.png'))
	)
	,
	controls.MessageInteractor(
		(window, 0, 0, 800, 600, vport, controls.Posattr((0, 200), (0, 30), (0, 250), (0, 250))),
		back=controls.Sprite(pyglet.resource.image('tbut.png')),
		front=controls.Sprite(pyglet.resource.image('tframe.png'))
	)
	,
	controls.Label(
		(window, 0, 0, 1, 1, vport, controls.Posattr((0.5, 0), (0.8, 0), (0, 0), (0, 0))),
		pyglet.text.Label(
			'SSSSSS', font_size=16, bold=True, anchor_x='center', anchor_y='center')
	)
	,
	controls.SpriteControl(
		(window, 0, 0, 1, 1, vport, controls.Posattr((0.6, 0), (0.8, 0), (0.1, 0), (0.1, 0))),
		controls.Sprite(pyglet.resource.image('tbut.png'))
	)
	,
	controls.MessageBox(
		(window, 0, 0, 800, 600, vport, controls.Posattr((0, 480), (0, 30), (0, 250), (0, 450))),
		back=controls.Sprite(pyglet.resource.image('tbut.png')),
		title=gtitle(),
		doc=gtxtbox()
	)
	,
	controls.AlertBox(
		(window, 0, 0, 800, 600, vport, controls.Posattr((0, 200), (0, 300), (0, 250), (0, 150))),
		back=controls.Sprite(pyglet.resource.image('tbut.png')),
		title=gtitle(),
		doc=gtxtbox(),
		button=gbutton()
	)
	,
	controls.MessageInput(
		(window, 0, 0, 800, 600, vport, controls.Posattr((0, 750), (0, 30), (0, 250), (0, 150))),
		back=controls.Sprite(pyglet.resource.image('tbut.png')),
		title=gtitle(),
		doc=geditbox(),
		button=gbutton()
	)
	,
	gscrollbar()
	,
	controls.TagPages(
		(window, 0, 0, 800, 600, vport, controls.Posattr((0, 750), (0, 200), (0, 250), (0, 200))),
		layouter=controls.TagPages_defaultlayoutH
	)
]

button1, txtbox1, prog, sbutton0, slider0, msg, lbl, img, msg1, alrt, inp, sld0, tagp = vport.sons

tagp.pages = [
	(gsbutton(), controls.ScrollTextBox([window], geditbox(), gscrollbar())),
	(gsbutton(), geditbox()),
	(gsbutton(), gbutton()),
	(gsbutton(), gsbutton()),
	(gsbutton(), gtxtbox())
]
slider0.buttons = [
	controls.SwitchButton(
		(window, 0, 0, 1, 1, slider0),
		images=[
			controls.Sprite(pyglet.resource.image('sliderf0.png')),
			controls.Sprite(pyglet.resource.image('sliderf1.png'))
		]
	)
	for i in range(10)
]
msg.sons = [
	controls.Button(
		(window, 25, 15, 150, 30, root, controls.Posattr((0, 50), (0, 30), (0, 150), (0, 30))),
		pyglet.text.Label('提交', font_name='微软雅黑', font_size=16, anchor_x='center', anchor_y='center'),
		controls.Sprite(pyglet.resource.image('tbut.png')),
		controls.Sprite(pyglet.resource.image('tico.png'))
	)
	,
	controls.TextBox(
		(window, 0, 0, 1, 1, vport, controls.Posattr((0, 50), (0, 65), (0, 150), (0, 150))),
		'''写在这里的文字会提交到左侧''',
		{'color': (0, 0, 200, 255), 'font_name': '仿宋', 'font_size': 14, 'line_spacing': 24, 'wrap': 'char'},
		editable=True, multiline=True,
		back=controls.Sprite(pyglet.resource.image('tbut.png')), select_backcolor=(0, 0, 200, 127)
	)
]
submitb, intertxt = msg.sons
msg.submit_key = (submitb, 'on_press')

msg1.buttons = [gbutton(), gbutton(), gbutton()]
# button1.label.text = '111'
# print(button1.text)
# button1.text = '11'
BALL_SOUND = pyglet.resource.media('ball.wav', streaming=False)
BGM = pyglet.resource.media('bgm.mp3', streaming=False)
bgm_player = BGM.play()


def lop():
	print('23')
	bgm_player.queue(BGM)
	bgm_player.next_source()


bgm_player.on_source_group_eos = lop


def onp():
	print('pressed button 0')
	BALL_SOUND.play()
	if button0.text == '隐藏其它':
		button0.text = '显示其它'
		bgm_player.pause()
	else:
		button0.text = '隐藏其它'
		bgm_player.play()
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
	print(len(alrt.sons))
	alrt.title = None
	alrt.doc = None
	alrt.button = None
	msg1.doc = None
	msg1.title = None


def onp1():
	print('pressed button 1')
	# print(button1.text)
	# button1.text = '11'
	prog.rate = (prog.rate + 0.1 - (prog.rate + 0.1) // 1)
	prog.text = '%.1f%%' % (prog.rate * 100)


def onps():
	print('pressed sbutton switch')
	sbutton0.stage ^= 1


def onschange(val):
	print('slider changed:new val = %s' % val)


def onsubmit():
	print()
	print('submitted')
	msg.hide()
	txtbox1.text = intertxt.text


# def onsubmit1(result):
# print('submitted msg1')
# msg1.hide()
# print(msg1.result)

button0.on_press = onp
button1.on_press = onp1
sbutton0.on_press = onps
slider0.on_change = onschange
msg.on_submit = onsubmit
# msg1.on_submit = onsubmit1

# TST = controls.SpriteControl([window],controls.Sprite(pyglet.resource.animation('walk.gif')))
# root.sons.append(TST)

# print(bat.__dict__)
for i in range(50):
	b = gbutton()
	vport.sons.append(gbutton())

# print(bat.__dict__)

window.show()
pyglet.app.run()
