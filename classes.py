class Node:
    def __init__(self, text, root = None):
        self._text = "\n".join( filter( lambda x:not x.lstrip().startswith("%"), text.splitlines() ) ) + "\n"
        self._index = 0
        self.root = root
        self.symbols = [ ["\\",-1], ["{",-1], ["}",-1], ["$",-1], ["%",-1], ["~",-1] ]

    @property
    def text(self):
        return self._text[self.index:]
    
    @text.setter
    def text(self, text):
        raise ValueError("text is a constant and should not be changed")
    
    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        if index < self._index:
            print("index overload: the index has been reset")
            self._index = len(self._text)
        else:
            self._index = index

    @property
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

    def move_index(self, text_to_find):
        self.index = self._text.find(text_to_find, self.index) + len(text_to_find)


class Source:

    def __init__(self, text):
        self.head = Node(text)
    
    # <<< treat this class as the actual head of the node
    def __getattr__(self, name):
        if name == "head":
            return self.head
        elif name == "index":
            return self.head.index
        elif name == "text":
            return self.head.text
        elif name == "inter":
            return self.head.inter
        else:
            return self.head.__dict__[name]

    def __setattr__(self, name, value):
        if name == "head":
            self.__dict__[name] = value
        elif name == "index":
            self.head.index = value
        elif name == "text":
            self.head.text = value
        else:
            self.head.__dict__[name] = value

    def move_index(self, text_to_find):
        self.head.move_index(text_to_find)
    # >>>

    def add(self, text):
        self.head = Node(text, self.head)

    def pop(self):
        self.head = self.head.root

class Clean:

    def __init__(self):
        self._text = []
        # aggessive mode, we are going to store all the skipped command in one .txt file
        self.aggro = set()
    
    def add(self, text):
        self._text.append(text)
    
    @property
    def text(self):
        return ''.join(self._text)
        
    @text.setter
    def text(self, text):
        self._text = [text]