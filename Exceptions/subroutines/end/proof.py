tt = 1
while writeEnd[-tt] != ' ' and writeEnd[-tt] != '\n':
    tt = tt+1
writeEnd = writeEnd[:-tt] + ' ■\n'
