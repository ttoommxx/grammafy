exceptions = [e[:-3] for e in os.listdir("./exceptions/subroutines/end/")]

dicSub = {'writeEnd':str}

t = 1
while readText[t] != '}':
    t = t+1
t = t+1 # skip the end of brackets for begin

command = "./exceptions/subroutines/end/" + readText[1:t-1] + ".py"
if os.path.exists(command):
    dicSub['writeEnd'] = writeText
    exec(open(command).read(),dicSub)
    writeText = dicSub['writeEnd']
j = j + t
