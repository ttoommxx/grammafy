tt = 0 #this time I already removed the brackets, I know I am calling a begin function

if asterisk:
    while readBegin[tt:tt+12] != '\\end{align*}':
        tt = tt+1
    t = t+tt+12
else:
    while readBegin[tt:tt+11] != '\\end{align}':
        tt = tt+1
    t = t+tt+11

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
