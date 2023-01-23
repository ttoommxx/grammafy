# find the index where the whole portion ends
i = SOURCE.find('\\end{thebibliography}') + 21
 
SOURCE = SOURCE[i:]
