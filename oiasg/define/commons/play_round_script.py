{
	'PLAY_ROUND_SCRIPT':
'''
event_queue = []
time = start_time + (((time - start_time) // time_delta) + 1) * time_delta
gamepage.refresh_time()
'''
}