events.update({
	'example_event': event(
		appearance=None,
		trigger='True # rand_expect(10)',
		effects={
			'immediate':
				'print("test_event")\n' +
				'trigger_event("example_event_triggered")\n'
			,
			'options': [
				{
					'name': 'option1',
					'effect': ''
				},
				{
					'name': 'option2',
					'effect': ''
				}
			]
		}
	),
	'example_event_triggered': event(
		appearance=None,
		trigger=None,
		effects={
			'immediate':
				'print("test_event_triggered")\n'
		}
	)
})
