class Permission(object):
    def __init__(self, key, name):
        self.key = key
        self.name = name
        self.children = []

    def append_child(self, child):
        self.children.append(child)
