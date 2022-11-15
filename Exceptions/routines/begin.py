import os

# behave similarly to the main, just create a list of what could be
exceptions = [e[:-3] for e in os.listdir("./exceptions/subroutines/begin/")]

dicSub = {'t':int, 'readBegin':str, 'writeBegin':str}

t = 1
while readText[t] != '}':
    t = t+1
t = t+1 # skip the end of brackets for begin

command = "./exceptions/subroutines/begin/" + readText[1:t-1] + ".py"
if os.path.exists(command):
    dicSub['t'] = t
    dicSub['readBegin'] = readText[t:]
    dicSub['writeBegin'] = writeText
    exec(open(command).read(),dicSub)
    t = dicSub['t']
    writeText = dicSub['writeBegin']
else:
    print('error 404: "' + readText[1:t-1] + '" not found in ./Exceptions/subroutines/begin/')
    # we do a loop to find end of the missing package and skip the section entirely
    k = t
    while readText[k:k+6+len(readText[1:t-1])] != '\\end{'+readText[1:t-1]+'}':
        k = k+1
    t = k+6+len(readText[1:t-1])
j = j + t
