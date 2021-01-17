class Animal:
    def __init__(self, an_type, color):
        self.an_type = an_type
        self.color = color

    def characteristic(self):
        return self.an_type + " " + self.color


class Wolf(Animal):
    def wolf_say(self):
        print("R-r-r-r")


class Snake(Animal):
    def snake_say(self):
        print("S-s-s-s")


class Goose(Animal):
    def goose_say(self):
        print("Ga-ga-ga")


class Cat(Animal):
    def cat_say(self):
        print("Meow-meow")


class Sheep(Animal):
    def sheep_say(self):
        print("Be-e-e-e")


if __name__ == '__main__':

    my_animals = [Wolf("Wolf", "gray"),
                  Snake("Snake", "green"),
                  Goose("Goose", "white"),
                  Cat("Cat", "black"),
                  Sheep("Sheep", "white")]

    for animal in my_animals:
        print(animal.characteristic())
        getattr(animal, f'{animal.__class__.__name__.lower()}_say')()
        print()
