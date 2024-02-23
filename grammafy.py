""" necessary modules """
import os
import sys
import argparse
import re
from typing import TypeVar
from classes import Source, Clean
from exceptions import interpret

SourceVar = TypeVar("SourceVar")
CleanVar = TypeVar("CleanVar")
EnvVar = TypeVar("EnvVar")


class Environment:
    """class to hold the environement variables"""

    def __init__(
        self, source: SourceVar, clean: CleanVar, folder_path: str, command: str = ""
    ):
        self.source = source
        self.clean = clean
        self.folder_path = folder_path
        self.command = command


parser = argparse.ArgumentParser(prog="grammafy", description="clean up tex files")
parser.add_argument("-c", "--commandline", help="select via command line argument")
args = parser.parse_args()  # args.picker contains the modality
if not args.commandline:
    import pyle_manager

    print("Press enter to pick a tex file")
    pyle_manager.get_key()
    file_path = pyle_manager.main("-p")
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

FOLDER_PATH = f"{os.path.dirname(file_path)}{os.sep}"

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

# initialise the final text
CLEAN = Clean()

# copy the main .tex file to a string
with open(file_path, encoding="utf-8") as SOURCE:
    SOURCE = Source(SOURCE.read())

# find the beginning of the document
if "\\begin{document}" not in SOURCE.text:
    print("\\begin{document} missing")
else:
    SOURCE.move_index("\\begin{document}")

ENV = Environment(SOURCE, CLEAN, FOLDER_PATH)

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
    f"{FOLDER_PATH}{FILE_NAME}_grammafied.txt", "w", encoding="utf-8"
) as file_output:
    file_output.write(ENV.clean.text)
    print(f"File written successfully, check {FOLDER_PATH}{FILE_NAME}_grammafied.txt")

if any(ENV.clean.aggro):
    print(f"Unknown commands, please check {FILE_NAME}_unknowns.txt")
    with open(
        f"{FOLDER_PATH}{FILE_NAME}_unknowns.txt", "w", encoding="utf-8"
    ) as file_unknowns:
        file_unknowns.write(str(ENV.clean.aggro))
