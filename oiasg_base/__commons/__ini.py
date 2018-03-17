import datetime
import random

# definition

val = lambda x: eval(x, globals(), globals())
exe = lambda x: exec(x, globals(), globals())

time = datetime.datetime
timed = datetime.timedelta

rand_expect = (lambda x: random.randint(0, x) == 0)


class event(object):
	def __init__(self, appearance=None, trigger=None, effects=None, user=None):
		self.appearance = appearance
		self.trigger = trigger
		self.effects = effects
		self.user = user
		if self.effects is not None:
			self.options = self.effects.get('options')
			self.immediate = self.effects.get('immediate')

	def check(self):
		if self.trigger is None:
			return False
		return val(self.trigger)

	def execute_options(self, option_chosen):
		if self.options is not None:
			for i in range(self.options.len()):
				if option_chosen[i]:
					exe(self.options[i]['effect'])

	def execute(self):
		if self.immediate is not None:
			exe(self.immediate)
		if self.appearance is not None:
			exe(self.appearance)
		# options

		# class problem(object):
		# def __init__(self, tags):
		# self.tags = tags
		# self.sols = {}


class contest(object):
	def __init__(self, appearance=None, problems=None, strategies=None, user=None):
		self.appearance = appearance
		self.problems = problems
		self.strategies = strategies
		self.user = user

		self.strategy = None
		self.running = False

	def start(self):
		self.running = True
		self.cur_problems = list(map(val, self.problems))
		global cur_timedelta, cur_contest
		cur_contest = self
		cur_timedelta = contest_timedelta

	def end(self):
		self.running = False
		global cur_timedelta, cur_contest
		cur_contest = None
		cur_timedelta = round_timedelta


class game_log(object):
	pass


check_event = lambda e: events[e].check()
execute_event = lambda e: events[e].execute()
trigger_event = lambda e: event_q.append(events[e])
execute_event_options = lambda e, o: events[e].execute_options(o)


def end():
	global running, event_q
	running = False
	event_q.clear()


# system

start_time = time(2016, 9, 1, 7)
cur_time = start_time
round_timedelta = timed(hours=8)
contest_timedelta = timed(minutes=1)
cur_timedelta = round_timedelta
end_time = time(2016, 9, 5, 7)
events = {}
contests = {}
log = game_log()
event_q = []
cur_contest = None
strategies = {}
timetable_menu = []
timetable = []
timetable_it = None


def play_round():
	global cur_time
	global event_q
	cur_time = start_time + (((cur_time - start_time) // cur_timedelta) + 1) * cur_timedelta
	print(cur_time)
	event_q.clear()
	for e in events.values():
		if e.check():
			event_q.append(e)
	global timetable_it
	if cur_contest is None and timetable_it is not None:
		event_q.append(events[strategies[timetable[timetable_it]]])
		timetable_it = (timetable_it + 1) % timetable.len()
	elif cur_contest is not None and cur_contest.strategy is not None:
		event_q.append(events[strategies[cur_contest.strategy]])
	event_q.sort(key=lambda x: x.user['privilege'] if x.user is not None and 'privilege' in x.user else -2147483648)
	while event_q:
		e = event_q[-1]
		event_q.pop()
		e.execute()


# abilities

thinking = {}
code = {}
tags = {}
ideas = {}
moods = {}
