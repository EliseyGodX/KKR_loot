class Student:
    def __init__(self, name: str, l):
        self.name = name
        self.l = l

    def e(self):
        return f'text {self.name}'

lst = {'a': Student('a', 'l'), 'b': Student('q', 'r')}
print(lst['b'].e())