class Node:
    def __init__(self, word):
        self.word = word
        self.left = None
        self.right = None

    def add(self, word):
        if word < self.word:
            if self.left is None:
                self.left = Node(word)
            else:
                self.left.add(word)
        elif word > self.word:
            if self.right is None:
                self.right = Node(word)
            else:
                self.right.add(word)
        # if word == self.word, ignore duplicate

    def print_in_order(self):
        if self.left is not None:
            self.left.print_in_order()

        print(self.word)

        if self.right is not None:
            self.right.print_in_order()

class POS_Tree:
    def __init__(self, word):
        self.root = Node(word)

    def add(self, word):
        self.root.add(word)

    def printTree(self):
        self.root.print_in_order()

    def smallest(self):
        curr = self.root
        while curr.left is not None:
            curr = curr.left
        return curr.word

tree = POS_Tree("f")
tree.add("c")
tree.add("d")
tree.add("g")
tree.add("h")
tree.add("i")
tree.printTree()