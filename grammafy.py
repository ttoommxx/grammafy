""" necessary modules """
import os
import sys
import argparse
import re
from classes import Source, Clean
from exceptions import interpret

parser = argparse.ArgumentParser(prog="grammafy", description="clean up tex files")
parser.add_argument("-c", "--commandline", help="select via command line argument")
args = parser.parse_args() # args.picker contains the modality
if not args.commandline:
    import pyle_manager
    pyle_manager.clear()
    print("Press enter to pick a tex file")
    pyle_manager.get_key()
    file_path = pyle_manager.main("-p")
    pyle_manager.clear()
else:
    file_path = args.commandline

FILE_NAME = ""
if not file_path:
    sys.exit("File not selected")
elif not file_path.endswith(".tex"):
    if input("The file selected is not in a tex format, enter Y to continue anyway. ").lower() != "y":
        sys.exit("Grammification interrupted")
    else:
        FILE_NAME = os.path.basename(file_path)
else:
    FILE_NAME = os.path.basename(file_path)[:-4]
if not FILE_NAME:
    sys.exit("Error fetching the file name")

folder_path = f"{os.path.dirname(file_path)}{os.sep}"

# list of admissible characters for commands
end_command = (" ","{","}",".",",",":",";","[","]","(",")","$","\\","\n","\"","'","~")

# initialise the final text
CLEAN = Clean()

# copy the main .tex file to a string
with open(file_path, encoding="utf-8") as SOURCE:
    SOURCE = Source( SOURCE.read() )

# find the beginning of the document
if "\\begin{document}" not in SOURCE.text:
    print("\\begin{document} missing")
else:
    SOURCE.move_index("\\begin{document}")

# start analysing the text
while SOURCE.head: # if any such element occurs
    next_index = SOURCE.inter
    if next_index is False:
        CLEAN.add(SOURCE.text)
        SOURCE.pop()
        continue
    
    # we can immediately add what we skipped before any interactive element
    CLEAN.add(SOURCE.text[:next_index])
    SOURCE.index += next_index

    match SOURCE.text[0]:
        case "\\": # FROM HERE - MAKE IT INTO A MATCH and include all this into the interpret if possible
            i = min( ( SOURCE.text.find(x,1) for x in end_command if x in SOURCE.text[1:] ) )  # take note of the index of such element
            command = SOURCE.text[ 1:i ]
            SOURCE.index += i
            # execute the routines
            interpret(SOURCE, CLEAN, command, folder_path)
        case "~":
            SOURCE.index += 1
            CLEAN.add(" ")
        case "{":
            SOURCE.index += 1
        case "}":
            SOURCE.index += 1
        case "$":
            CLEAN.add("[_]")
            SOURCE.index += 1
            if SOURCE.text[0] == "$":
                SOURCE.move_index("$$")
            else: # assuming there are no double dollars within one-dollar equations
                SOURCE.move_index("$")
        case "%":
            SOURCE.move_index("\n")
        case _:
            if input(f"Fatal error, unknown interactive {SOURCE.text[0]}. \
                    Press Y to continue or any other button to abort").lower() != "y":
                sys.exit("Aborted")
            else:
                SOURCE.index += 1


# CLEANING ROUTINES
# trailing spaces
CLEAN.text = CLEAN.text.strip()
# unmatched brackets and tabs
CLEAN.text = CLEAN.text.replace("[]", "").replace("()", "").replace("\t", " ")
# pointless spaces
CLEAN.text = re.sub(r"( )*\n( )*", "\n", CLEAN.text)
# too many lines
CLEAN.text = re.sub(r"\n\n\s*", "\n\n", CLEAN.text)
# dourble spacing
CLEAN.text = re.sub(r"( )+", " ", CLEAN.text)
# remove new line before [_] unless preceded by -
CLEAN.text = re.sub(r"(\S)\n?(?<!-)\[_\]", r"\1 [_]", CLEAN.text)
# remove new line after [_] unless followed by bulletpoint
CLEAN.text = re.sub(
    r"\[_\](\.|,|;)?\n(?!(?:\d+\.|-))(\S)", r"[_]\1 \2", CLEAN.text)


with open(f"{folder_path}{FILE_NAME}_grammafied.txt","w", encoding="utf-8") as file_output:
    file_output.write(CLEAN.text)
    print(f"File written successfully, check {folder_path}{FILE_NAME}_grammafied.txt")

if any(CLEAN.aggro):
    print(f"Unknown commands, please check {FILE_NAME}_unknowns.txt")
    with open(f"{folder_path}{FILE_NAME}_unknowns.txt","w", encoding="utf-8") as file_unknowns:    
        file_unknowns.write(str(CLEAN.aggro))
