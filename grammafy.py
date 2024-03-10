"""necessary modules"""

import os
import sys
import argparse
import re
from classes import Source, Clean
from exceptions import interpret


parser = argparse.ArgumentParser(prog="grammafy", description="clean up tex files")
parser.add_argument("-c", "--commandline", help="select via command line argument")
args = parser.parse_args()  # args.picker contains the modality
if not args.commandline:
    import pyle_manager

    input("Press enter to pick a tex file")
    file_path = pyle_manager.file_manager("-p")
else:
    file_path = args.commandline

FILE_NAME = ""
if not file_path:
    sys.exit("File not selected")
elif not file_path.endswith(".tex"):
    if (
        input(
            "The file selected is not in a tex format, enter Y to continue anyway. "
        ).lower()
        != "y"
    ):
        sys.exit("Grammification interrupted")
    else:
        FILE_NAME = os.path.basename(file_path)
else:
    FILE_NAME = os.path.basename(file_path)[:-4]

if not FILE_NAME:
    sys.exit("Error fetching the file name")

# list of admissible characters for commands
end_command = (
    " ",
    "{",
    "}",
    ".",
    ",",
    ":",
    ";",
    "[",
    "]",
    "(",
    ")",
    "$",
    "\\",
    "\n",
    '"',
    "'",
    "~",
)


class Environment:
    """class to hold the environement variables"""

    def __init__(self):
        with open(file_path, encoding="utf-8") as source_file:
            self.source = Source(source_file.read())
        self.clean = Clean()
        self.folder_path = f"{os.path.dirname(file_path)}{os.sep}"
        self.command = ""


ENV = Environment()


# copy the main .tex file to a string

# find the beginning of the document
if "\\begin{document}" not in ENV.source.text:
    print("\\begin{document} missing")
else:
    ENV.source.move_index("\\begin{document}")


# start analysing the text
while ENV.source.head:  # if any such element occurs
    next_index = ENV.source.inter
    if next_index is False:
        ENV.clean.add(ENV.source.text)
        ENV.source.pop()
        continue

    # we can immediately add what we skipped before any interactive element
    ENV.clean.add(ENV.source.text[:next_index])
    ENV.source.index += next_index

    match ENV.source.text[0]:
        case "\\":  # FROM HERE - MAKE IT INTO A MATCH and include all this into the interpret if possible
            i = min(
                (
                    ENV.source.text.find(x, 1)
                    for x in end_command
                    if x in ENV.source.text[1:]
                )
            )  # take note of the index of such element
            ENV.command = ENV.source.text[1:i]
            ENV.source.index += i
            # execute the routines
            interpret(ENV)
        case "~":
            ENV.source.index += 1
            ENV.clean.add(" ")
        case "{":
            ENV.source.index += 1
        case "}":
            ENV.source.index += 1
        case "$":
            ENV.clean.add("[_]")
            ENV.source.index += 1
            if ENV.source.text[0] == "$":
                ENV.source.move_index("$$")
            else:  # assuming there are no double dollars within one-dollar equations
                ENV.source.move_index("$")
        case "%":
            ENV.source.move_index("\n")
        case _:
            if (
                input(
                    f"Fatal error, unknown interactive {ENV.source.text[0]}. \
                    Press Y to continue or any other button to abort"
                ).lower()
                != "y"
            ):
                sys.exit("Aborted")
            else:
                ENV.source.index += 1


# CLEANING ROUTINES
# trailing spaces
ENV.clean.text = ENV.clean.text.strip()
# unmatched brackets and tabs
ENV.clean.text = ENV.clean.text.replace("[]", "").replace("()", "").replace("\t", " ")
# pointless spaces
ENV.clean.text = re.sub(r"( )*\n( )*", "\n", ENV.clean.text)
# too many lines
ENV.clean.text = re.sub(r"\n\n\s*", "\n\n", ENV.clean.text)
# dourble spacing
ENV.clean.text = re.sub(r"( )+", " ", ENV.clean.text)
# remove new line before [_] unless preceded by -
ENV.clean.text = re.sub(r"(\S)\n?(?<!-)\[_\]", r"\1 [_]", ENV.clean.text)
# remove new line after [_] unless followed by bulletpoint
ENV.clean.text = re.sub(
    r"\[_\](\.|,|;)?\n(?!(?:\d+\.|-))(\S)", r"[_]\1 \2", ENV.clean.text
)


with open(
    f"{ENV.folder_path}{FILE_NAME}_grammafied.txt", "w", encoding="utf-8"
) as file_output:
    file_output.write(ENV.clean.text)
    print(
        f"File written successfully, check {ENV.folder_path}{FILE_NAME}_grammafied.txt"
    )

if any(ENV.clean.aggro):
    print(f"Unknown commands, please check {FILE_NAME}_unknowns.txt")
    with open(
        f"{ENV.folder_path}{FILE_NAME}_unknowns.txt", "w", encoding="utf-8"
    ) as file_unknowns:
        file_unknowns.write(str(ENV.clean.aggro))
