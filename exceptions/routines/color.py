t = 1 # skip opening brackets
writeText = writeText + 'Color:'
while readText[t] != '}':
	writeText = writeText + readText[t].upper()
	t = t+1
j = j+t