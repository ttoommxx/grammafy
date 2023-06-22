# find the index where the whole portion ends
i = SOURCE[-2].find("\\end{thebibliography}",SOURCE[-1]) + 21
 
SOURCE[-1] = i
