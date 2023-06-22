CLEAN += "Color:"
i = SOURCE[-2].find( "}",next_elem ) + 1
CLEAN += SOURCE[-2][ next_elem+6:i-1 ].upper()
SOURCE[-1] = i