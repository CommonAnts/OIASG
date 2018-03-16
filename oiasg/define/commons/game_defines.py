{
	'GAME_TIME_INTERVAL':[0,2,1,0.5,0.2,0.05],
	'GAME_DEFINE':{
		# 游戏的预定义文件 -- 定义一局游戏的初始数据
		'general':{
			# 游戏开始时间
			'start_time':datetime.datetime(2016,1,1,0),
			# 游戏结束时间
			'end_time':datetime.datetime(2018,1,1,0),
			# 正常情况下的时间变化量（比赛等特殊情况除外）
			'time_delta':datetime.timedelta(hours = 1),
			# 角色
			'CHARACTER':{
				'name':'CommonAnts',
				'image':'commonants_icon.png',
				'data':{
					'province':'陕西省',
					'school':'某少女附中',
					'birth':datetime.datetime(2001,7,11),
				}
			}
		}
	},
	'GENERAL_GAME_DEFINE':{
		# 所有游戏通用的预定义文件
		
		# 基本数据集
		'events':{},
		'strategies':{},
		'abilities':{},
		'abilitypages':{},
		'messages':{},
		'contests':{},
		
		# 子集
		'timetable_messages':[],
		'log_messages':[],
		
		'strategy_plans':[],
		'strategy_plan_it':0,
		'current_strategy':None,
		
		'select_strategies':[],
		
		'pages_character_back':None,
		'pages_character_front':None,
	}
}