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
        file_name = os.path.basename(file_path)
else:
    file_name = os.path.basename(file_path)[:-4]

if os.name == "nt":
    folder_path = f"{os.path.dirname(file_path)}\\"
elif os.name == "posix":
    folder_path = f"{os.path.dirname(file_path)}/"
else:
    sys.exit("Operating system not recognised")

# list of admissible characters for commands
end_command = (" ","{","}",".",",",":",";","[","]","(",")","$","\\","\n","\"","'","~")

# initialise the final text
clean = Clean()

# copy the main .tex file to a string
with open(file_path) as source_temp:
    source = Source( source_temp.read() )

# find the beginning of the document
if "\\begin{document}" not in source.text:
    print("\\begin{document} missing")
else:
    source.move_index("\\begin{document}")

# start analysing the text
while source: # if any such element occurs
    next_index = source.inter()
    if next_index is False:
        clean.text += source.text
        source = source.root
        continue
    
    clean.text += source.text[:next_index] # we can immediately add what we skipped before any interactive element
    source.index += next_index

    match source.text[0]:
        case "\\": # FROM HERE - MAKE IT INTO A MATCH and include all this into the interpret if possible
            i = min( ( source.text.find(x,1) for x in end_command if x in source.text[1:] ) )  # take note of the index of such element
            command = source.text[ 1:i ]
            source.index += i
            # execute the routines
            interpret(source, clean, command, folder_path)
        case "~":
            source.index += 1
            clean.text += " "
        case "{":
            source.index += 1
        case "}":
            source.index += 1
        case "$":
            clean.text += "[_]"
            source.index += 1
            if source.text[0] == "$":
                source.move_index("$$")
            else: # assuming there are no double dollars within one-dollar equations
                source.move_index("$")
        case "%":
            source.move_index("\n")
        case _:
            if input(f"Fatal error, unknown interactive {source.text[0]}. \
                    Press Y to continue or any other button to abort").lower() != "y":
                sys.exit("Aborted")
            else:
                source.index += 1


# CLEANING ROUTINES
# trailing spaces
clean.text = clean.text.strip()
# unmatched brackets and tabs
clean.text = clean.text.replace("[]","").replace("()","").replace("\t"," ")
# pointless spaces
clean.text = re.sub("( )*\n( )*", "\n", clean.text)
# too many lines
clean.text = re.sub("\n\n\s*", "\n\n", clean.text)
# dourble spacing
clean.text = re.sub("( )+", " ", clean.text)
# remove new line before [_] unless preceded by -
clean.text = re.sub("(\S)\n?(?<!-)\[_\]", r"\1 [_]", clean.text)
# remove new line after [_] unless followed by bulletpoint
clean.text = re.sub("\[_\](\.|,|;)?\n(?!(?:\d+\.|-))(\S)", r"[_]\1 \2", clean.text) 


with open(f"{folder_path}{file_name}_grammafied.txt","w") as file_output:
    file_output.write(clean.text)

if any(clean.aggro):
    print(f"Unknown commands, please check {file_name}_list_unknowns.txt")
    with open(f"{folder_path}{file_name}_list_unknowns.txt","w") as file_unknowns:    
        file_unknowns.write(str(clean.aggro))