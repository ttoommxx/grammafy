# the following function prints the line from str file containing the y-th letter
def line_printer(str,y):
    return(str[str.rfind('\n',0,y)+2 : str.find('\n',y)])
