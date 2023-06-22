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
def inter(string):
    try:
        return min( ((x, string.find(x)) for x in list_inter if x in string), key = lambda x:x[1] )
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

SOURCE = [] # last entry is the index, the penultimum is the string

# copy the main .tex file to a string
with open(file_path) as SOURCE_TEMP:
    SOURCE.append( SOURCE_TEMP.read() )
    SOURCE.append( 0 )

# find the beginning of the document
if "\\begin{document}" not in SOURCE[-2]:
    print("\\begin{document} missing")
else:
    SOURCE[-1] = SOURCE[-2].find("\\begin{document}") + 16 # we start from right after "\\begin{document}"

# FROM HERE

# so far works only when the files to include belong to the same folder
# while "\include{" in SOURCE:
#     i = SOURCE.find("\include{") # the string will start at position i+9
#     j = SOURCE.find("}",i+9)
#     include_path = SOURCE[i+9:j]
#     if not include_path.endswith(".tex"): # if the extension is not present
#         include_path = f"{include_path}.tex"
#     with open(folder_path + include_path) as INCLUDE:
#         SOURCE = SOURCE[:i] + INCLUDE.read() + SOURCE[j+1:]

# while "\input{" in SOURCE:
#     i = SOURCE.find("\input{") # the string will start at position i+7
#     j = SOURCE.find("}",i+7)
#     include_path = SOURCE[i+7:j]
#     if not include_path.endswith(".tex"): # if the extension is not present
#         include_path = f"{include_path}.tex"
#     with open(folder_path + include_path) as INCLUDE:
#         SOURCE = SOURCE[:i] + INCLUDE.read() + SOURCE[j+1:]

# start analysing the text
while SOURCE: # if any such element occurs
    elem = inter( SOURCE[-2][ SOURCE[-1]: ] )
    if not elem:
        CLEAN += SOURCE[-2][ SOURCE[-1]: ]
        del SOURCE[-2:]
        continue

    CLEAN += SOURCE[-2][ SOURCE[-1]:SOURCE[-1]+elem[1] ] # we can immediately add what we skipped before any interactive element
    next_elem = SOURCE[-1]+elem[1]+1

    match elem[0]:
        case "\\": # FROM HERE - MAKE IT INTO A MATCH
            if SOURCE[-2][ next_elem ] == "[": # equation
                i = SOURCE[-2].find("\]", next_elem ) + 3
                CLEAN += "[_]"
                if SOURCE[-2][ next_elem:i-3 ].replace(" ","").replace("\n","")[-1] in [",", ";", "."]: # add punctuation to non-inline equations
                    CLEAN += SOURCE[-2][ next_elem:i-3 ].replace(" ","").replace("\n","")[-1]
                SOURCE[-1] = i
            elif SOURCE[-2][ next_elem ] == "&":
                CLEAN += "&"
                SOURCE[-1] = next_elem+1
            elif SOURCE[-2][ next_elem ] == " ": # space
                SOURCE[-1] = next_elem
            elif SOURCE[-2][ next_elem ] == "\"":
                CLEAN += "\""
                SOURCE[-1] = next_elem+1
            elif SOURCE[-2][ next_elem ] == "\\": # new line
                CLEAN += "\n"
                SOURCE[-1] = next_elem+1
            elif SOURCE[-2][ next_elem ] == "'":
                if SOURCE[-2][ next_elem+1 ] in ["a","e","i","o","u"]:
                    CLEAN += SOURCE[-2][ next_elem+1 ] + u"\u0301" # unicode encoding
                    SOURCE[-1] = next_elem+2
                else:
                    CLEAN += "'"
                    SOURCE[-1] = next_elem+1
            else:
                i = min( [ SOURCE[-2].find(x,next_elem) for x in end_command if x in SOURCE[-2][next_elem:] ] )  # take note of the index of such element
                command_name = SOURCE[-2][ next_elem:i ]
                if SOURCE[-2][i] == "*":
                    i+=1
                SOURCE[-1] = i
                if os.path.exists(f"./exceptions/routines_custom/{command_name}.py"): # first I search within custom subroutines
                    exec(open(f"./exceptions/routines_custom/{command_name}.py").read())
                elif os.path.exists(f"./exceptions/routines/{command_name}.py"): # then I search within built-in subroutines
                    exec(open(f"./exceptions/routines/{command_name}.py").read())
                elif command_name in void:
                    pass
                else:
                    while SOURCE[-2][i] in ["{","["]: # check if opening and closing brackets
                        i += 1
                        j = i # index for open brackets
                        while i >= j:
                            i = min([SOURCE[-2].find(x,i) for x in ["}","]"] if x in SOURCE[-2][i:] ])+1
                            j = min([SOURCE[-2].find(x,j) for x in ["{","["] if x in SOURCE[-2][j:] ] , default=i+1)+1
                    # the explanation of the above is a little complicated: I look for a (the first) closed bracket and a (the first) open bracket. They must match, otherwise it would contradict the fact that they are the first. I keep doing it until I can't find an open one. So min will be set to i and we would break out of the internal while. As for the external, every time I get out I look for the adjacent bracket and there is another one I iterate!
                    SOURCE[-1] = i
                    list_aggro.add(command_name)
        case "~":
            SOURCE[-1] = next_elem
        case "{":
            SOURCE[-1] = next_elem
        case "}":
            SOURCE[-1] = next_elem
        case "$":
            if SOURCE[-2][ next_elem ] == "$":
                i = SOURCE[-2].find( "$$",next_elem+1 ) + 2
            else: # assuming there are no double dollars within one-dollar equations
                i = SOURCE[-2].find( "$",next_elem+1 ) + 1
            CLEAN += "[_]"
            # TO DO, ADD COMMAS ETC IF THAT'S HOW THE EQUATION ENDS
            SOURCE[-1] = i
        case "%":
            SOURCE[-1] = SOURCE[-2].find( "\n",next_elem ) + 1
        case _:
            if input(f"Fatal error, unknown interactive {SOURCE[-2][elem[0]]}. \
                     Press Y to continue or any other button to abort").lower() != "y":
                sys.exit("Aborted")
            else:
                SOURCE[-1] = next_elem

# CLEANING ROUTINES
# remove unmatched brackets and tabbing with spaces
CLEAN = CLEAN.replace("[]","").replace("()","").replace("\t"," ")
# remove initial spaces and newlines
while len(CLEAN)>0 and CLEAN[0] in ["\n"," "]:
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
