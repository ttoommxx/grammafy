# so far works only when the files to include belong to the same folder

import os

t = readText.find('}')
include_path = readText[1:t-1]
if include_path[-4:] != '.tex': # if the extension is not present
    include_path = include_path + '.tex'

# we add to the previous source the included source
included_text = open(path_main + include_path, 'r')
text = included_text.read()
included_text.close()
readText = text + readText[t:]