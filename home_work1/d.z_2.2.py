# Aggregation
class Strings:
    def __init__(self):
        self.chords = ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"]
        print(self.chords)


class Guitar:
    def __init__(self, strings):
        self.strings = strings


strings = Strings()
guitar = Guitar(strings)

