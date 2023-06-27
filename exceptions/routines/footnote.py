i = 1
j = i # index for open brackets
while i >= j and j > 0 :
    i = source.tex.find( "}",i ) +1
    j = source.tex.find( "{",j ) +1

# add the text in the footnote to the queue in parenthesis
source = source.add("(FOOTNOTE: " + source.tex[ 1:i-1 ] + ")")
source.root.index += i
