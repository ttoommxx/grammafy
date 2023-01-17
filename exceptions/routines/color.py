writeText = writeText + 'Color:'
i = readText.find('}') + 1
writeText = writeText + readText[1:i-1].upper()
readText = readText[i:]