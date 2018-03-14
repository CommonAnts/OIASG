{
	'PLAY_ROUND_SCRIPT':
'''
time = start_time + (((time - start_time) // time_delta) + 1) * time_delta
dispatch_game_event('on_update_speed_time')

event_queue = []

for key, value in events.items():
	if value.check(game):
		event_queue.append(value)
event_queue.sort(key = lambda x:x.privilege)

if event_queue:
	event = event_queue[-1]
	event_queue.pop()
	event.exe(game)
'''
}