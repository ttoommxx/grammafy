class Node:
    def __init__(self, text, root = None):
        self._text = "\n".join( filter( lambda x:not x.lstrip().startswith("%"), text.splitlines() ) ) + "\n"
        self._index = 0
        self.root = root
        self.symbols = [ ["\\",-1], ["{",-1], ["}",-1], ["$",-1], ["%",-1], ["~",-1] ]

    @property
    def text(self):
        return self._text[self.index:]
    
    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        if index < self._index:
            print("Index has been reset because attempt of making it smaller")
            self._index = len(self._text)
        else:
            self._index = index

    def move_index(self, text_to_find):
        self.index = self._text.find(text_to_find, self.index) + len(text_to_find)

    def inter(self):
        # this trick is so that if I remove an element from the list I don't intact the next one cause it is going backwards
        for x in self.symbols[::-1]:
            if x[1] < self.index: # update only those that haven't been used    
                if x[0] not in self.text:
                    self.symbols.remove(x)
                else:
                    x[1] = self._text.find(x[0], self.index)
        if any(self.symbols):
            return min( x[1] for x in self.symbols) - self.index
        else:
            return False

class Source:

    def __init__(self, text):
        self.head = Node(text)
    
    # <<< inherit properties from node  
    @property
    def root(self):
        return self.head.root

    @property
    def index(self):
        return self.head.index

    @index.setter
    def index(self, index):
        self.head.index = index

    @property
    def text(self):
        return self.head.text

    def move_index(self, text_to_find):
        self.head.move_index(text_to_find)
            
    def inter(self):
        return self.head.inter()
    # >>>

    def add(self, text):
        self.head = Node(text, self.head)

    def pop(self):
        self.head = self.head.root

class Clean:

    def __init__(self, text = ""):
        self.text = text
        # aggessive mode, we are going to store all the skipped command in one .txt file
        self.aggro = set()