import re

f = open('ideas.md', 'r', encoding = 'utf-8').readlines()

def pr(id, name):
	print(
'''
	%s:{
		'name':'%s',
		'appearance':None,
		'relations':{},
		'privilege':0,
		'level':0,
	}''' % (id,name))

print('''ideas.update({
''')
it = 0

for r in f:
	print('\t,')
	pr(it,r.strip())
	it += 1

print('''})
''')

