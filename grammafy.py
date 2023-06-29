import os, sys, argparse, re
from Source import Source

parser = argparse.ArgumentParser(prog="grammafy", description="clean up tex files")
parser.add_argument("-c", "--commandline", help="select via command line argument")
args = parser.parse_args() # args.picker contains the modality
if not args.commandline:
    import pyleManager
    pyleManager.clear()
    input("Press enter to pick a tex file")
    file_path = pyleManager.main("-p")
    pyleManager.clear()
else:
    file_path = args.commandline

if not file_path:
    sys.exit("File not selected")
elif not file_path.endswith(".tex"):
    if input("the file selected is not in a tex format, enter Y to continue anyway. ").lower() != "y":
        sys.exit("the file selected is not a tex file")
else:
    print(f"{file_path} selected")    

# aggessive mode, we are going to store all the skipped command in one .txt file
list_aggro = set()
list_log_command = set()

# we now store information on the file path
file_name = os.path.basename(file_path)[:-4]
folder_path = f"{os.path.dirname(file_path)}/"

# create a list of existing exceptions
exceptions = (e[:-3] for e in os.listdir("./exceptions/routines/"))
exceptions_custom = (e[:-3] for e in os.listdir("./exceptions/routines_custom/"))

# fetch list of commands that should not produce any text output
with open("./exceptions/void.txt") as void_list, open("./exceptions/void_custom.txt","r") as void_custom_list:
    void = [line.strip() for line in void_list.readlines()] \
        + [line.strip() for line in void_custom_list.readlines()] # put them together as it doesn't make a difference, there is no overriding

# list of admissible characters for commands
end_command = (" ","{","}",".",",",":",";","*","[","]","(",")","$","\\","\n")

# initialise the final text
clean = ""

# copy the main .tex file to a string
with open(file_path) as source_temp:
    source = Source( source_temp.read() )

# find the beginning of the document
if "\\begin{document}" not in source.tex:
    print("\\begin{document} missing")
else:
    source.move_index("\\begin{document}")

# start analysing the text
while source: # if any such element occurs
    next_index = source.inter()
    if next_index is False:
        clean += source.tex
        source = source.root
        continue
    
    clean += source.tex[:next_index] # we can immediately add what we skipped before any interactive element
    source.index += next_index

    match source.tex[0]:
        case "\\": # FROM HERE - MAKE IT INTO A MATCH
            if source.tex[1] == "[": # equation
                i = source.tex.find( "\\]" )
                clean += "[_]"
                if source.tex[:i].rstrip()[-1] in [",", ";", "."]: # add punctuation to non-inline equations
                    clean += source.tex[:i].rstrip()[-1]
                source.move_index( "\\]" )
            elif source.tex[1] == "(":
                i = source.tex.find( "\\)" )
                clean += "[_]"
                if source.tex[:i].rstrip()[-1] in [",", ";", "."]:
                    clean += source.tex[:i].rstrip()[-1]
                source.move_index( "\\)" )
            elif source.tex[1] == "&":
                clean += "&"
                source.index += 2
            elif source.tex[1] == " ": # space
                source.index += 1
            elif source.tex[1] == "\"":
                if source.tex[2] not in ["a","e","i","o","u"]:
                    clean += "\""
                source.index += 2
            elif source.tex[1] == "\\": # new line
                clean += "\n"
                source.index += 2
            elif source.tex[1] == "%":
                clean += "%"
                source.index += 2
            elif source.tex[1] == "'":
                if source.tex[2] not in ["a","e","i","o","u"]:
                    clean += "'"
                source.index += 2
            elif source.tex[1] == "#":
                clean += "#"
                source.index += 2
            else:
                i = min( ( source.tex.find(x,1) for x in end_command if x in source.tex[1:] ) )  # take note of the index of such element
                command_name = source.tex[ 1:i ]

                if source.tex[i] == "*":
                    i += 1
                source.index += i

                if os.path.exists(f"./exceptions/routines_custom/{command_name}.py"): # first I search within custom subroutines
                    exec(open(f"./exceptions/routines_custom/{command_name}.py").read())
                elif os.path.exists(f"./exceptions/routines/{command_name}.py"): # then I search within built-in subroutines
                    exec(open(f"./exceptions/routines/{command_name}.py").read())
                elif command_name in void:
                    pass
                else:
                    while source.tex[0] in ["{","["]: # check if opening and closing brackets
                        if source.tex[0] == "{":
                            i = source.tex.find("{",1)
                            j = source.tex.find("}",1)
                            while 0 < i < j:
                                i = source.tex.find("{",i+1)
                                j = source.tex.find("}",j+1)
                            source.index += j+1
                        else:
                            i = source.tex.find("[",1)
                            j = source.tex.find("]",1)
                            while 0 < i < j:
                                i = source.tex.find("[",i+1)
                                j = source.tex.find("]",j+1)
                            source.index += j+1
                    list_aggro.add(command_name)
        case "~":
            source.index += 1
        case "{":
            source.index += 1
        case "}":
            source.index += 1
        case "$":
            clean += "[_]"
            source.index += 1
            if source.tex[0] == "$":
                source.move_index("$$")
            else: # assuming there are no double dollars within one-dollar equations
                source.move_index("$")
        case "%":
            source.move_index("\n")
        case _:
            if input(f"Fatal error, unknown interactive {source.tex[0]}. \
                    Press Y to continue or any other button to abort").lower() != "y":
                sys.exit("Aborted")
            else:
                source.index += 1

# CLEANING ROUTINES
# trailing spaces
clean = clean.strip()
# unmatched brackets and tabs
clean = clean.replace("[]","").replace("()","").replace("\t"," ")
# pointless spaces
clean = re.sub("( )*\n( )*", "\n", clean)
# # too many lines
clean = re.sub("\n\n\s*", "\n\n", clean)
# # dourble spacing
clean = re.sub("( )+", " ", clean)
# # reset indentation for [_]
clean = re.sub("(\w|\.|,|;|:)\n?\[_\]", r"\1 [_]", clean)
clean = re.sub("\[_\](\.|,|;)?\n(?!\d.)(\w)", r"[_]\1 \2", clean)


with open(f"{folder_path}{file_name}_grammafied.txt","w") as file_output:
    file_output.write(clean)

if any(list_aggro):
    print(f"Unknown commands, please check {file_name}_list_unknowns.txt")
    with open(f"{folder_path}{file_name}_list_unknowns.txt","w") as file_unknowns:    
        file_unknowns.write(str(list_aggro))
if any(list_log_command):
    print(f"Unknown commands within commands, please check {file_name}_list_log_command.txt")
    with open(f"{folder_path}{file_name}_list_log_command.txt","w") as file_log_command:
        file_log_command.write(str(list_log_command))