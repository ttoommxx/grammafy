tt = 0 #this time I already removed the brackets, I know I am calling a begin function

if asterisk:
    while readBegin[tt:tt+15] != '\\end{equation*}':
        tt = tt+1
    t = t+tt+14
else:
    while readBegin[tt:tt+14] != '\\end{equation}':
        tt = tt+1
    t = t+tt+13

writeBegin = writeBegin + '[1]'
while readBegin[tt-1] == ' ' or readBegin[tt-1] == '\n':
    tt = tt-1
match readBegin[tt-1]:
    case ',':
        writeBegin = writeBegin + ','
    case ';':
        writeBegin = writeBegin + ';'
    case '.':
        writeBegin = writeBegin + '.'
