"""necessary modules"""

import os
import sys
import argparse
import re
from classes import Source, Clean
from exceptions import interpret


class Environment:
    """class to hold the environement variables"""

    def __init__(self, file_path: str) -> None:
        with open(file_path, encoding="utf-8") as source_file:
            self.source = Source(source_file.read())
        self.clean = Clean()
        self.folder_path = f"{os.path.dirname(file_path)}{os.sep}"
        self.command = ""


def grammafy(file_path: str = "") -> None:
    """main function to execute"""

    if not file_path:
        import pyle_manager

        input("Press enter to pick a tex file")
        file_path = pyle_manager.file_manager(True)

    file_name = ""
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
            file_name = os.path.basename(file_path)
    else:
        file_name = os.path.basename(file_path)[:-4]

    if not file_name:
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

    env = Environment(file_path)

    # copy the main .tex file to a string

    # find the beginning of the document
    if "\\begin{document}" not in env.source.text:
        print("\\begin{document} missing")
    else:
        env.source.move_index("\\begin{document}")

    # start analysing the text
    while env.source.head:  # if any such element occurs
        next_index = env.source.inter
        if next_index == -1:
            env.clean.add(env.source.text)
            env.source.pop()
            continue

        # we can immediately add what we skipped before any interactive element
        env.clean.add(env.source.text[:next_index])
        env.source.index += next_index

        match env.source.text[0]:
            case "\\":  # FROM HERE - MAKE IT INTO A MATCH and include all this into the interpret if possible
                i = min(
                    (
                        env.source.text.find(x, 1)
                        for x in end_command
                        if x in env.source.text[1:]
                    )
                )  # take note of the index of such element
                env.command = env.source.text[1:i]
                env.source.index += i
                # execute the routines
                interpret(env)
            case "~":
                env.source.index += 1
                env.clean.add(" ")
            case "{":
                env.source.index += 1
            case "}":
                env.source.index += 1
            case "$":
                env.clean.add("[_]")
                env.source.index += 1
                if env.source.text[0] == "$":
                    env.source.move_index("$$")
                else:  # assuming there are no double dollars within one-dollar equations
                    env.source.move_index("$")
            case "%":
                env.source.move_index("\n")
            case _:
                if (
                    input(
                        f"Fatal error, unknown interactive {env.source.text[0]}. \
                        Press Y to continue or any other button to abort"
                    ).lower()
                    != "y"
                ):
                    sys.exit("Aborted")
                else:
                    env.source.index += 1

    # CLEANING ROUTINES
    # trailing spaces
    env.clean.text = env.clean.text.strip()
    # unmatched brackets and tabs
    env.clean.text = (
        env.clean.text.replace("[]", "").replace("()", "").replace("\t", " ")
    )
    # pointless spaces
    env.clean.text = re.sub(r"( )*\n( )*", "\n", env.clean.text)
    # too many lines
    env.clean.text = re.sub(r"\n\n\s*", "\n\n", env.clean.text)
    # dourble spacing
    env.clean.text = re.sub(r"( )+", " ", env.clean.text)
    # remove new line before [_] unless preceded by -
    env.clean.text = re.sub(r"(\S)\n?(?<!-)\[_\]", r"\1 [_]", env.clean.text)
    # remove new line after [_] unless followed by bulletpoint
    env.clean.text = re.sub(
        r"\[_\](\.|,|;)?\n(?!(?:\d+\.|-))(\S)", r"[_]\1 \2", env.clean.text
    )

    with open(
        f"{env.folder_path}{file_name}_grammafied.txt", "w", encoding="utf-8"
    ) as file_output:
        file_output.write(env.clean.text)
        print(
            f"File written successfully, check {env.folder_path}{file_name}_grammafied.txt"
        )

    if any(env.clean.aggro):
        print(f"Unknown commands, please check {file_name}_unknowns.txt")
        with open(
            f"{env.folder_path}{file_name}_unknowns.txt", "w", encoding="utf-8"
        ) as file_unknowns:
            file_unknowns.write(str(env.clean.aggro))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="grammafy", description="clean up tex files")
    parser.add_argument("-c", "--commandline", help="select via command line argument")
    args = parser.parse_args()  # args.picker contains the modality
    grammafy(args.commandline)
