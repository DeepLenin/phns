class Node:
    def __init__(self, phoneme):
        self.children = []
        self.phoneme = phoneme

class Graph:
    def __init__(self):
        self.root = Node('<root>')

    def attach(self, pronunciations):
        if len(pronunciations) > 1:
        else:
            for pronunciations[0]

