CLEAN += "[_]"

# find the index where the whole portion ends
i = SOURCE.find("\\end{verbatim}")
if SOURCE[:i-1].replace(" ","").replace("\n","").replace("$","")[-1] in [",", ";", "."]:
                CLEAN += SOURCE[:i-1].replace(" ","").replace("\n","").replace("$","")[-1]

i = i + 14 # skipping to the end of the program 
SOURCE = SOURCE[i:]