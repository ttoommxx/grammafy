CLEAN += "[_]"

# find the index where the whole portion ends
i = min([SOURCE[-2].find(x,SOURCE[-1]) for x in ["\\end{gather*}", "\\end{gather}"] if x in SOURCE[-2][SOURCE[-1]:] ])
if SOURCE[-2][SOURCE[-1]:i-1].replace(" ","").replace("\n","").replace("$","")[-1] in [",", ";", "."]:
                CLEAN += SOURCE[-2][SOURCE[-1]:i-1].replace(" ","").replace("\n","").replace("$","")[-1]

i = i + 12 + (SOURCE[-2][SOURCE[-1] + 12] == "*") # skipping to the end of the program 
SOURCE[-1] = i