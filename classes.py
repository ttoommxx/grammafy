"""main objects used by grammafy main execution"""


class Node:
    """NodeList class contained source code to be cleaned, ordered from head"""

    def __init__(self, text, root=None):
        self._text = (
            "\n".join(
                filter(lambda x: not x.lstrip().startswith("%"), text.splitlines())
            )
            + "\n"
        )
        self._index = 0
        self.root = root
        self.symbols = {"\\": -1, "{": -1, "}": -1, "$": -1, "%": -1, "~": -1}

    @property
    def text(self) -> str:
        """return the text from the current index"""
        return self._text[self.index :]

    @text.setter
    def text(self, text: str) -> None:
        """does not allow for modifying the source code"""
        raise ValueError("text is a constant and should not be changed")

    @property
    def index(self) -> int:
        """return the current index"""
        return self._index

    @index.setter
    def index(self, index: int) -> None:
        """set the index and reset if analysing backwards, this way if functions are poorly programmer the script won't loop"""
        if index < self._index:
            print("index overload: the index has been reset")
            self._index = len(self._text)
        else:
            self._index = index

    @property
    def inter(self) -> bool | int:
        """this functions search for the first symbol occurrence that has already been analysed yet, i.e. that precedes the current index"""
        for x in list(self.symbols.keys()):
            if self.symbols[x] < self.index:  # update only those that haven't been used
                if x not in self.text:
                    self.symbols.pop(x)
                else:
                    self.symbols[x] = self._text.find(x, self.index)
        if any(self.symbols):
            return min(self.symbols.values()) - self.index
        else:
            return False

    def move_index(self, text_to_find: str) -> None:
        """search for text_to_find and move index at the end of the text"""
        self.index = self._text.find(text_to_find, self.index) + len(text_to_find)


class Source:
    """mock class that behaves like the head of the ListNode (inherits most of its attributes) and pops the head when it's been fully analysed"""

    def __init__(self, text: str):
        self.head = Node(text)

    # <<< treat this class as the actual head of the node
    def __getattr__(self, name: str):
        """inherits members of the Node class"""
        match name:
            case "head":
                return self.head
            case "index":
                return self.head.index
            case "text":
                return self.head.text
            case "inter":
                return self.head.inter
            case _:
                return self.head.__dict__[name]

    def __setattr__(self, name, value) -> None:
        """inherits members of the Node class"""
        match name:
            case "head":
                self.__dict__[name] = value
            case "index":
                self.head.index = value
            case "text":
                self.head.text = value
            case _:
                self.head.__dict__[name] = value

    def move_index(self, text_to_find: str) -> None:
        """inherits the move_index function from Node"""
        self.head.move_index(text_to_find)

    # >>>

    def add(self, text: str) -> None:
        """add a new node and set it as head"""
        self.head = Node(text, self.head)

    def pop(self) -> None:
        """remove the current node, keeping the object as is"""
        self.head = self.head.root


class Clean:
    """class that contains the cleaned up tex code"""

    def __init__(self):
        self._text = []
        # aggessive mode, we are going to store all the skipped command in one .txt file
        self.aggro = set()

    def add(self, text: str) -> None:
        """add new cleaned text"""
        self._text.append(text)

    @property
    def text(self) -> str:
        """when being called, it assembles the code that has been added and returns it, keeping it in memory in case its called again"""
        if len(self._text) > 1:
            self._text = ["".join(self._text)]
        return self._text[0]

    @text.setter
    def text(self, text: str) -> None:
        """when setting the text, it clears the queue"""
        self._text = [text]
