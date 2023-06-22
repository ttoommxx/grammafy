# included files need to be in the same folder

i = SOURCE[-2].find("}", SOURCE[-1])
include_path = SOURCE[-2][ SOURCE[-1]+1:i ]
if not include_path.endswith(".tex"): # if the extension is not present
    include_path = f"{include_path}.tex"
with open(f"{folder_path}{include_path}") as INCLUDE:
    SOURCE.append( INCLUDE.read() )
    SOURCE.append(0)
SOURCE[-3] = i+1
