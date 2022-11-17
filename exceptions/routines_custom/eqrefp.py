t = 1 # skip opening brackets
while readText[t] != '}':
	t = t+1
j = j+t
writeText = writeText + '[1]'