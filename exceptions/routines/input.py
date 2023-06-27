# included files need to be in the same folder

i = source.tex.find("}")
include_path = source.tex[ 1:i ]
if not include_path.endswith(".tex"): # if the extension is not present
    include_path += ".tex"
with open(f"{folder_path}{include_path}") as include_tex:
    source = source.add( include_tex.read() )
source.root.index += i+1
