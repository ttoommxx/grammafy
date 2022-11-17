t = 1 # skip opening brackets
while readText[t] != '}':
	t = t+1
# we expect another parenthesis
t = t+1
while readText[t] != '}':
	t = t+1
j = j+t