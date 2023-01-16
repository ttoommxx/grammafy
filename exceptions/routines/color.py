writeText = writeText + 'Color:'
i = readText.find('}') + 1
readText = readText[i:]
writeText = writeText + readText[1:i-2].upper()