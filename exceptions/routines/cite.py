t = 1 # skip opening brackets
while readText[t] != '}':
	t = t+1

writeText = writeText + '[1]'
j = j+t