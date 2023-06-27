class Source():

    def __init__(self, text = "", root_class = None):
        self._tex = ""
        for line in text.splitlines():
            if not line.lstrip().startswith("%"):
                self._tex += line + "\n"
        self.index = 0
        self.root = root_class
    
    @property
    def tex(self):
        return self._tex[self.index:]
    
    @tex.setter
    def tex(self,text):
        self._tex = text

    def move_index(self, text_to_find):
        if text_to_find not in self.tex: # go to the end
            self.index = len(self._tex)
        else:
            self.index = self._tex.find(text_to_find, self.index) + len(text_to_find)
    
    def add(self, text = ""):
        return Source(text, root_class = self)
        
    def inter(self):
        list_inter = ("\\","{","}","$","%","~") # types of different "command" headers
        try:
            return min( ( self._tex.find(x, self.index) for x in list_inter if x in self.tex ) ) - self.index
        except ValueError:
            return False
        