def clean_up(text):
    return "\n".join( filter( lambda x:not x.lstrip().startswith("%"), text.splitlines() ) ) + "\n"

list_inter = ("\\","{","}","$","%","~")

class Source():

    def __init__(self, text = "", root_class = None):
        self._text = clean_up(text)
        self.index = 0
        self.root = root_class

    @property
    def text(self):
        return self._text[self.index:]

    def move_index(self, text_to_find):
        if text_to_find not in self.text: # go to the end
            self.index = len(self._text)
        else:
            self.index = self._text.find(text_to_find, self.index) + len(text_to_find)
    
    def add(self, text = ""):
        self_root_copy = self.__dict__.copy()["root"]
        self.root = Source(self.text, self_root_copy)
        self._text = clean_up(text)
        self.index = 0
        
    def inter(self):
        # types of different "command" headers
        try:
            return min( ( self._text.find(x, self.index) for x in list_inter if x in self.text ) ) - self.index
        except ValueError:
            return False
        
class Clean():

    def __init__(self, text = ""):
        self.text = text
        # aggessive mode, we are going to store all the skipped command in one .txt file
        self.aggro = set()