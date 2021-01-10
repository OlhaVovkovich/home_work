# metaclass
class A:
    def print_a(self):
        print('a')


class B:
    def print_b(self):
        print('b')


class C:
    def print_c(self):
        print('c')


class StarMetaClass(type):
    def __new__(cls, name, parents, attr):
        parents = (A, B, C) + parents
        return type(name, parents, attr)


class Abc(metaclass=StarMetaClass):
    pass


abc = Abc()
abc.print_a()
abc.print_b()
abc.print_c()

