CLEAN += "[_]"

# find the index where the whole portion ends
i = min([SOURCE[-2].find(x,next_elem) for x in ["\\end{gather*}", "\\end{gather}"] if x in SOURCE[-2][next_elem:] ])
if SOURCE[-2][next_elem:i-1].replace(" ","").replace("\n","").replace("$","")[-1] in [",", ";", "."]:
                CLEAN += SOURCE[-2][next_elem:i-1].replace(" ","").replace("\n","").replace("$","")[-1]

i = i + 12 + (SOURCE[-2][next_elem+12] == "*") # skipping to the end of the program 
SOURCE[-1] = i