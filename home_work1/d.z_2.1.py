#Composition
class Laptop:
    def __init__(self):
        keyboard = Keyboard('This is keyboard')
        screen = Screen('This is screen')
        self.elements = [keyboard, screen]


class Keyboard:
    def __init__(self, color):
        self.color = color


class Screen:
    def __init__(self, size):
        self.size = size


prod = Laptop()
