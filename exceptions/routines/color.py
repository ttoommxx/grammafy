clean += "Color:"
i = source.tex.find( "}" )
clean += source.tex[ 1:i ].upper()
source.index += i+1