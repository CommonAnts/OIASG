import re

f = open('tags.md', 'r', encoding = 'utf-8').readlines()

def gettab(r):
	c = 0
	while r[0] == '\t':
		c += 1
		r = r[1:]
	return c,r

def pr(id, name, pa):
	print(
'''
	%s:{
		'name':'%s',
		'appearance':None,
		'parent':%s,
		'relations':{},
		'privilege':0,
		'difficulty':0,
		'level':0,
		'traits':{
			'structure':1,
			'graphic':1
		}
	}'''
		% (id,name,pa)
	)

print('''tags.update({
''')
stk = []
mp = []
dep = {}
it = 0

pr(it,'root','None')
stk.append(it)
dep[it] = -1
it += 1

for r in f:
	cnt,x = gettab(r)
	dep[it] = cnt
	x = x.split()
	x.pop(0)
	if x[-1][-1] == ')':
		n = re.sub('[^A-Z]','',x[-1])
		mp.append((n,it))
		x.pop()
	x = ''.join(x)
	while dep[stk[-1]] >= cnt:
		stk.pop()
	print('\t,')
	pr(it,x,stk[-1])
	stk.append(it)
	it += 1

print('''})
''')

for i in mp:
	print('%s = tags[%s]' % i)
	