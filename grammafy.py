import os,sys,time # import time if need to debug, time.sleep(seconds), remove sys once stopped debugging

import pyleManager
pyleManager.clear()
input("Press enter to pick a .tex file")
file_path = pyleManager.main("-p")
pyleManager.clear()

if not file_path:
    sys.exit("File not selected")
elif not file_path.endswith(".tex"):
    sys.exit("the file selected is not a tex file")
else:
    print(f"{file_path} selected")    

# aggessive mode, we are going to store all the skipped command in one .txt file
list_aggro = set()
list_log_command = set()

# we now store information on the file path
file_name = os.path.basename(file_path)[:-4]
folder_path = f"{os.path.dirname(file_path)}/"

# types of different "command" headers
list_inter = ("\\","{","}","$","%","~")
def inter():
    try:
        return min( ((x, SOURCE.find(x)) for x in list_inter if x in SOURCE), key = lambda x:x[1] )
    except ValueError:
        return False


# create a list of existing exceptions
exceptions = (e[:-3] for e in os.listdir("./exceptions/routines/"))
exceptions_custom = (e[:-3] for e in os.listdir("./exceptions/routines_custom/"))

# fetch list of commands that should not produce any text output
with open("./exceptions/void.txt") as void_list, open("./exceptions/void_custom.txt","r") as void_custom_list:
    void = [line.strip() for line in void_list.readlines()] + [line.strip() for line in void_custom_list.readlines()] # put them together as it doesn't make a difference, there is no overriding

# list of admissible characters for commands
end_command = (" ","{","}",".",",",":",";","*","[","]","(",")","$","\\","\n")

# initialise the final text
CLEAN = ""

# copy the main .tex file to a string
with open(file_path) as SOURCE_TEMP:
    SOURCE = SOURCE_TEMP.read()

# find the beginning of the document
if "\\begin{document}" not in SOURCE:
    print("\\begin{document} missing")
    i = 0 # we start from the beginning, probably it's an included .tex file
else:
    i = SOURCE.find("\\begin{document}") + 16 # we start from right after "\\begin{document}"
SOURCE = SOURCE[i:]

# remove comments first -- check if it is not preceeded by backslash
# while '%' in SOURCE:
#     SOURCE = SOURCE[:SOURCE.find('%')] + SOURCE[SOURCE.find('\n',SOURCE.find('%')+1) + 1:]

# so far works only when the files to include belong to the same folder
while "\include{" in SOURCE:
    i = SOURCE.find("\include{") # the string will start at position i+9
    j = SOURCE.find("}",i+9)
    include_path = SOURCE[i+9:j]
    if not include_path.endswith(".tex"): # if the extension is not present
        include_path = f"{include_path}.tex"
    with open(folder_path + include_path) as INCLUDE:
        SOURCE = SOURCE[:i] + INCLUDE.read() + SOURCE[j+1:]

while "\input{" in SOURCE:
    i = SOURCE.find("\input{") # the string will start at position i+7
    j = SOURCE.find("}",i+7)
    include_path = SOURCE[i+7:j]
    if not include_path.endswith(".tex"): # if the extension is not present
        include_path = f"{include_path}.tex"
    with open(folder_path + include_path) as INCLUDE:
        SOURCE = SOURCE[:i] + INCLUDE.read() + SOURCE[j+1:]

# start analysing the text
while le := inter(): # if any such element occurs
    i = le[1]
        
    CLEAN += SOURCE[:i] # we can immediately add what we skipped before any interactive element
    SOURCE = SOURCE[i:] # remove the clean part from SOURCE
    match le[0]:
        case "\\":
            if SOURCE[1] == "[": # equation
                i = SOURCE.find("\]",1) + 3
                CLEAN += "[_]"
                if SOURCE[:i-3].replace(" ","").replace("\n","")[-1] in [",", ";", "."]: # add punctuation to non-inline equations
                    CLEAN = CLEAN + SOURCE[:i-3].replace(" ","").replace("\n","")[-1]
                SOURCE = SOURCE[i:]
            elif SOURCE[1] == "&":
                CLEAN += "&"
                SOURCE = SOURCE[2:]
            elif SOURCE[1] == " ": # space
                SOURCE = SOURCE[1:]
            elif SOURCE[1] == "\"":
                CLEAN += "\""
                SOURCE = SOURCE[2:]
            elif SOURCE[1] == "\\": # new line
                CLEAN = CLEAN + "\n"
                SOURCE = SOURCE[2:]
            elif SOURCE[1] == "'":
                if SOURCE[2] in ["a","e","i","o","u"]:
                    CLEAN += SOURCE[2] + u"\u0301" # unicode encoding
                    SOURCE = SOURCE[3:]
                else:
                    CLEAN = CLEAN + "'"
                    SOURCE = SOURCE[2:]
            else:
                i = min( [ SOURCE.find(x,1) for x in end_command if x in SOURCE[1:] ] )  # take note of the index of such element
                command_name = SOURCE[1:i]
                SOURCE = SOURCE[i + (SOURCE[i]=="*"):]
                if os.path.exists(f"./exceptions/routines_custom/{command_name}.py"): # first I search within custom subroutines
                    exec(open(f"./exceptions/routines_custom/{command_name}.py").read())
                elif os.path.exists(f"./exceptions/routines/{command_name}.py"): # then I search within built-in subroutines
                    exec(open(f"./exceptions/routines/{command_name}.py").read())
                elif command_name in void:
                    pass
                else:
                    i = 0 # index for closed brackets
                    while SOURCE[i] in ["{","["]:
                        i = i+1
                        j = i # index for open brackets
                        while i >= j:
                            i = min([SOURCE.find(x,i) for x in ["}","]"] if x in SOURCE[i:] ])+1
                            j = min([SOURCE.find(x,j) for x in ["{","["] if x in SOURCE[j:] ] , default=i+1)+1
                    # the explanation of the above is a little complicated: I look for a (the first) closed bracket and a (the first) open bracket. They must match, otherwise it would contradict the fact that they are the first. I keep doing it until I can't find an open one. So min will be set to i and we would break out of the internal while. As for the external, every time I get out I look for the adjacent bracket and there is another one I iterate!
                    SOURCE = SOURCE[i:]
                    list_aggro.add(command_name)
        case "~":
            SOURCE = SOURCE[1:]
        case "{":
            SOURCE = SOURCE[1:]
        case "}":
            SOURCE = SOURCE[1:]
        case "$":
            if SOURCE[1] == "$":
                i = SOURCE.find("$$",2) + 2
            else: # assuming there are no double dollars within one-dollar equations
                i = SOURCE.find("$",1) + 1
            CLEAN += "[_]"
            # TO DO, ADD COMMAS ETC IF THAT'S HOW THE EQUATION ENDS
            SOURCE = SOURCE[i:]
        case "%":
            SOURCE = SOURCE[SOURCE.find("\n") + 1:]
        case _:
            print("Fatal error, unknown interactive")

# CLEANING ROUTINES
# remove unmatched brackets and tabbing with spaces
CLEAN = CLEAN.replace("[]","").replace("()","").replace("\t"," ")
# remove initial spaces and newlines
while CLEAN[0] in ["\n"," "]:
    CLEAN = CLEAN[1:]
# remove newline+space preliminarly to the cleaning
while "\n " in CLEAN:
    CLEAN = CLEAN.replace("\n ","\n")
# reset indentation for [_]s
while "\n[_]" in CLEAN or "[_]\n" in CLEAN or "[_],\n" in CLEAN or "[_].\n" in CLEAN or "[_];\n" in CLEAN:
    CLEAN = CLEAN.replace("\n[_]"," [_]").replace("[_]\n","[_] ").replace("[_],\n","[_], ").replace("[_].\n","[_]. ").replace("[_];\n","[_]; ")
# add some space before every [_] in case we have them attached to something else
CLEAN = CLEAN.replace(".[_]",". [_]".replace(",[_]",", [_]")).replace(";[_]","; [_]")
while "\n\n\n" in CLEAN or "  " in CLEAN or " -" in CLEAN: # remove double lines and double spaces
    CLEAN = CLEAN.replace("\n\n\n","\n\n").replace("  "," ").replace(" -","\n-")

with open(f"{folder_path}{file_name}_grammafied.txt","w") as file_output:
    file_output.write(CLEAN)

if any(list_aggro):
    print(f"Unknown commands, please check {file_name}_list_unknowns.txt")
    with open(f"{folder_path}{file_name}_list_unknowns.txt","w") as file_unknowns:    
        file_unknowns.write(str(list_aggro))
if any(list_log_command):
    print(f"Unknown commands within commands, please check {file_name}_list_log_command.txt")
    with open(f"{folder_path}{file_name}_list_log_command.txt","w") as file_log_command:
        file_log_command.write(str(list_log_command))

from platform import system
if system() == 'Linux':
    os.system("xdg-open " + f"{folder_path}{file_name}_grammafied.txt".replace(' ','\ '))
