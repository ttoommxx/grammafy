import os

def curly(source, clean, command):
    source.move_index("}")

def curly_curly(source, clean, command):
    source.move_index("}")
    source.move_index("}")

def color(source, clean, command):
    clean.tex += "Color:"
    i = source.tex.find( "}" )
    clean.tex += source.tex[ 1:i ].upper()
    source.index += i+1

def dash(source, clean, command):
    clean.tex += "-"

def footnote(source, clean, command):
    i = 1
    j = i # index for open brackets
    while i >= j and j > 0 :
        i = source.tex.find( "}",i ) +1
        j = source.tex.find( "{",j ) +1

    # add the text in the footnote to the queue in parenthesis
    source.add("(FOOTNOTE: " + source.tex[ 1:i-1 ] + ")")
    source.root.index += i

def include(source, clean, command): # included files need to be in the same folder
    i = source.tex.find("}")
    include_path = source.tex[ 1:i ]
    if not include_path.endswith(".tex"): # if the extension is not present
        include_path += ".tex"
    with open(f"{folder_path}{include_path}") as include_tex:
        source.add( include_tex.read() )
    source.root.index += i+1

def print_curly(source, clean, command):
    clean.tex += "[_]"
    source.move_index("}")

def print_square_curly(source, clean, command):
    clean.tex += "[_]"
    if source.tex[0] == "[":
        source.move_index("]")
    source.move_index("}")

def begin(source, clean, command): # from here
    # behave similarly to the main, just create a list of what could be
    i = source.tex.find("}") # right next after the brackets
    command = source.tex[ 1:i ] # remove asterisk if any
    source.move_index("}")

    if os.path.exists(f"./exceptions/subroutines/begin_custom/{command}.py"):
        exec(open(f"./exceptions/subroutines/begin_custom/{command}.py").read())
    elif os.path.exists(f"./exceptions/subroutines/begin/{command}.py"):
        exec(open(f"./exceptions/subroutines/begin/{command}.py").read())
    elif command not in void_begin:
        # do someething here like skip the command entirely by looking at where \end{command + asterisk if any} is. proble is incapsulated commands, so maybe best strategy is do nothing
        clean.log_command.add(command)
        if asterisk:
            command += "*"
        i = 0
        j = i
        j_alert = i
        while i >= j and j_alert>-1:
            i = source.tex.find("\\end{" + command + "}",i) + 6 + len(command)
            j_alert = source.tex.find("\\begin{" + command + "}",j)
            j = j_alert + 8 + len(command)
            
        source.index += i
        
def end(source, clean, commmand): # from here
    exceptions = (e[:-3] for e in os.listdir("./exceptions/subroutines/end/"))

    i = source.tex.find("}")

    asterisk = source.tex[i-1] == "*"
    command = source.tex[1:i-asterisk] # remove asterisk if any
    # command = "./exceptions/subroutines/end/" + command + ".py"

    source.move_index("}")

    # if os.path.exists(command):
    #     exec(open(command,'r').read())


    if os.path.exists(f"./exceptions/subroutines/end_custom/{command}.py"):
        exec(open(f"./exceptions/subroutines/end_custom/{command}.py").read())
    elif os.path.exists(f"./exceptions/subroutines/end/{command}.py"):
        exec(open(f"./exceptions/subroutines/end/{command}.py").read())