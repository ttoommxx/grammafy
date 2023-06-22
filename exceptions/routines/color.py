CLEAN += "Color:"
i = SOURCE[-2].find( "}",SOURCE[-1] ) + 1
CLEAN += SOURCE[-2][ SOURCE[-1]+1:i-1 ].upper()
SOURCE[-1] = i