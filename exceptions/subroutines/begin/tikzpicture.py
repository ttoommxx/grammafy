tt = 0 #this time I already removed the brackets, I know I am calling a begin function

while readBegin[tt:tt+17] != '\\end{tikzpicture}':
    tt = tt+1
t = t+tt+17

writeBegin = writeBegin + '[1]'
while readBegin[tt-1] in [' ', '\n']:
    tt = tt-1
match readBegin[tt-1]:
    case ',':
        writeBegin = writeBegin + ','
    case ';':
        writeBegin = writeBegin + ';'
    case '.':
        writeBegin = writeBegin + '.'
