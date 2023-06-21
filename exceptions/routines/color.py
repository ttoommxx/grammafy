CLEAN += "Color:"
i = SOURCE.find("}") + 1
CLEAN += SOURCE[1:i-1].upper()
SOURCE = SOURCE[i:]