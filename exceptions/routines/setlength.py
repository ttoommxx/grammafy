i = readText.find('}')+1
i = readText[i:].find('}') + i + 1
readText = readText[i:]