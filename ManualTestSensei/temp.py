from dataclasses import dataclass

@dataclass
class Parent:
    def print_class(self):
        print(self.__class__)

@dataclass
class Sibling(Parent):
    pass

if __name__ == '__main__':
    s = Sibling()
    s.print_class()
