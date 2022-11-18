tt = 0 #this time I already removed the brackets, I know I am calling a begin function

while readBegin[tt:tt+12] != '\\end{figure}':
    tt = tt+1
t = t+tt+12

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
