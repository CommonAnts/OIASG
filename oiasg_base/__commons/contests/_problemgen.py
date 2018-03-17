def problem_basic(name):
	return {
		'name': name,
		'tags': {
			0: {
				'parents': None,
				'parent': None,
				'score': 30,
				'tag': AB['name'],
				'relations': {
					134: 1.0  # AB
				},
				'difficulty': 0.5,
				'rate': 0
			},
			1: {
				'parents': [0],
				'parent': None,
				'score': 70,
				'tag': FT['name'],
				'relations': {
					144: 1.0  # FFT
				},
				'difficulty': 2,
				'rate': 0
			}
		},
		'sols': {}
	}
