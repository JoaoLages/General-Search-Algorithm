class Stack:

    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __repr__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_size(self):
        return self.size
