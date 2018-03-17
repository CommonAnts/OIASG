events.update({
	'check_timeline': event(
		appearance=None,
		trigger='cur_time > end_time',
		effects={
			'immediate':
				'''
				print("Game has ended:time up.")
				end()
				'''
		},
		user={'privilege': 2147483647}
	)
})
