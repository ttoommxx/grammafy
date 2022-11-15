tt = 0 #this time I already removed the brackets, I know I am calling a begin function

while readBegin[tt:tt+15] != '\\end{equation*}':
    tt = tt+1
t = t+tt+14

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
