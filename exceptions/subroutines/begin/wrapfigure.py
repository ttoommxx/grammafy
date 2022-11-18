tt = 0
while readBegin[tt] != '}':
	tt = tt+1
# we expect another parenthesis
tt = tt+1
while readBegin[tt] != '}':
	tt = tt+1
# and another one
tt = tt+1
while readBegin[tt] != '}':
	tt = tt+1
t = t + tt