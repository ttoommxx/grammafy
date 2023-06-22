# find the index where the whole portion ends
i = SOURCE[-2].find("\\end{thebibliography}",next_elem) + 21
 
SOURCE[-1] = i
