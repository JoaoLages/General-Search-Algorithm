class Cask:

    def __init__(self, name, size, weight):
        self.name = name
        self.size = size
        self.weight = weight

    def __repr__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_size(self):
        return self.size

    def get_weight(self):
        return self.weight
