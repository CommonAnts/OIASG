{
	'EVENTS':{
		0:{
			'trigger':'True',
			'effect':'''
pages_character_back = 'default.png'

pages_character_front = 'commonants_image.png'
			
messages[cnt] = MessageItem(name = '测试信息TMessage %s' % cnt, text = '测试文本\\n啦啦啦啦啦啦', image = 'orz.gif')

log_messages.append(cnt)

timetable_messages.append(cnt)

strategy_plans = [key for key in strategies.keys()]

select_strategies = list(strategies.keys())

cnt+=1;ui.Alert_Notitle(str(cnt)+str(current_strategy)).exe()
''',
			'privilege':0
		}
	}
}