from unittest import mock


class Test:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def hello(self):
        return 1


def new_test():
    return Test()


def func():
    with new_test() as t:
        return t.hello()