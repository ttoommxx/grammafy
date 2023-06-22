CLEAN += "[_]"

# find the index where the whole portion ends
i = SOURCE[-2].find("\\end{tikzpicture}",next_elem)
if SOURCE[-2][next_elem:i-1].replace(" ","").replace("\n","").replace("$","")[-1] in [",", ";", "."]:
                CLEAN += SOURCE[-2][next_elem:i-1].replace(" ","").replace("\n","").replace("$","")[-1]

i = i + 17 # skipping to the end of the program 
SOURCE[-1] = i
