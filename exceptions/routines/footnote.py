i = 1
j = i # index for open brackets
while i >= j and j > 0 :
    i = SOURCE[-2].find( "}",SOURCE[-1]+i ) +1
    j = SOURCE[-2].find( "{",SOURCE[-1]+j ) +1

# add the text in the footnote to the queue in parenthesis
SOURCE.append( "(FOOTNOTE: " + SOURCE[-2][SOURCE[-1]+1:i-1] + ")")
SOURCE.append(0)
SOURCE[-3] += i-1
