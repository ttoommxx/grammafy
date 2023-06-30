import os, sys, argparse, re
from classes import Source, Clean
from exceptions import interpret

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

# we now store information on the file path
file_name = os.path.basename(file_path)[:-4]
folder_path = f"{os.path.dirname(file_path)}/"

# list of admissible characters for commands
end_command = (" ","{","}",".",",",":",";","*","[","]","(",")","$","\\","\n")

# initialise the final text
clean = Clean()

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
        clean.tex += source.tex
        source = source.root
        continue
    
    clean.tex += source.tex[:next_index] # we can immediately add what we skipped before any interactive element
    source.index += next_index

    match source.tex[0]:
        case "\\": # FROM HERE - MAKE IT INTO A MATCH and include all this into the interpret if possible
            if source.tex[1] == "[": # equation
                i = source.tex.find( "\\]" )
                clean.tex += "[_]"
                if source.tex[:i].rstrip()[-1] in [",", ";", "."]: # add punctuation to non-inline equations
                    clean.tex += source.tex[:i].rstrip()[-1]
                source.move_index( "\\]" )
            elif source.tex[1] == "(":
                i = source.tex.find( "\\)" )
                clean.tex += "[_]"
                if source.tex[:i].rstrip()[-1] in [",", ";", "."]:
                    clean.tex += source.tex[:i].rstrip()[-1]
                source.move_index( "\\)" )
            elif source.tex[1] == "&":
                clean.tex += "&"
                source.index += 2
            elif source.tex[1] == " ": # space
                source.index += 1
            elif source.tex[1] == "\"":
                if source.tex[2] not in ["a","e","i","o","u"]:
                    clean.tex += "\""
                source.index += 2
            elif source.tex[1] == "\\": # new line
                clean.tex += "\n"
                source.index += 2
            elif source.tex[1] == "%":
                clean.tex += "%"
                source.index += 2
            elif source.tex[1] == "'":
                if source.tex[2] not in ["a","e","i","o","u"]:
                    clean.tex += "'"
                source.index += 2
            elif source.tex[1] == "#":
                clean.tex += "#"
                source.index += 2
            else:
                i = min( ( source.tex.find(x,1) for x in end_command if x in source.tex[1:] ) )  # take note of the index of such element
                command = source.tex[ 1:i ]

                if source.tex[i] == "*":
                    i += 1
                source.index += i

                interpret(source, clean, command, folder_path)
        case "~":
            source.index += 1
        case "{":
            source.index += 1
        case "}":
            source.index += 1
        case "$":
            clean.tex += "[_]"
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
clean.tex = clean.tex.strip()
# unmatched brackets and tabs
clean.tex = clean.tex.replace("[]","").replace("()","").replace("\t"," ")
# pointless spaces
clean.tex = re.sub("( )*\n( )*", "\n", clean.tex)
# too many lines
clean.tex = re.sub("\n\n\s*", "\n\n", clean.tex)
# dourble spacing
clean.tex = re.sub("( )+", " ", clean.tex)
# remove new line before [_] unless preceded by -
clean.tex = re.sub("(\S)\n?(?<!-)\[_\]", r"\1 [_]", clean.tex)
# remove new line after [_] unless followed by bulletpoint
clean.tex = re.sub("\[_\](\.|,|;)?\n(?!(?:\d+\.|-))(\S)", r"[_]\1 \2", clean.tex) 


with open(f"{folder_path}{file_name}_grammafied.txt","w") as file_output:
    file_output.write(clean.tex)

if any(clean.aggro):
    print(f"Unknown commands, please check {file_name}_list_unknowns.txt")
    with open(f"{folder_path}{file_name}_list_unknowns.txt","w") as file_unknowns:    
        file_unknowns.write(str(clean.aggro))