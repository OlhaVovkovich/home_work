from abc import ABC, abstractmethod, abstractproperty
from bisect import bisect
from functools import total_ordering


@total_ordering
class House:
    def __init__(self, area: int, cost: int):
        self.area = area
        self.cost = cost

    def __lt__(self, other):
        if isinstance(other, int):
            return self.cost < other
        elif isinstance(other, House):
            return self.cost < other.cost

        raise ValueError('Should be an instance of int or House')

    def __eq__(self, other):
        if isinstance(other, int):
            return self.cost == other
        elif isinstance(other, House):
            return self.cost == other.cost

        raise ValueError('Should be an instance of int or House')

    def __str__(self):
        return f'House(cost={self.cost}, area={self.area})'

    def apply_discount(self, discount):
        self.cost *= 1 - discount


class Human(ABC):

    @abstractmethod
    def info_myself(self):
        pass

    @abstractmethod
    def buy_a_house(self):
        pass

    @abstractmethod
    def make_money(self):
        pass


class Person (Human):
    def __init__(self, name: str, age: int, av_money: int, salary: int, house: House = None):
        self.name = name
        self.age = age
        self.av_money = av_money
        self.salary = salary
        self.house = house

    @property
    def has_home(self):
        return bool(self.house)

    def info_myself(self):
        print(f'{self.name}, {self.age}, av_money: {self.av_money}, has home: {self.has_home}')

    def buy_a_house(self, realtor):
        """buys the most expensive house he can afford"""
        realtor.make_money(client=self)

        if self.has_home:
            print("Congrat on buying a house")
        else:
            print("Sorry, you don't have enough money")

    def make_money(self):
        self.av_money += self.salary


class Realtor(Person):
    DISCOUNT_AREA = 40  # m ** 2
    DISCOUNT = .03      # 3 %

    def __new__(cls, name: str, age: int, av_money: int, salary: int, houses: list[House], *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Realtor, cls).__new__(cls, *args, **kwargs)
            cls.init = False
        return cls.instance

    def __init__(self, name: str, age: int, av_money: int, salary: int, houses: list[House]):
        if not self.init:
            self.init = True

            super().__init__(name, age, av_money, salary)
            self.houses = houses
            self.houses.sort()

    def inf_about_houses(self):
        for i in range(len(self.houses)):
            print(f'House #{i}: area = {self.houses[i].area} m2, cost = ${self.houses[i].cost}')

    def discount(self, house: House):
        house.apply_discount(self.DISCOUNT)

    def make_money(self, client: Person):
        house_idx = bisect(self.houses, client.av_money) - 1

        # boundary conditions
        if house_idx >= len(self.houses):
            house_idx = -1
        elif house_idx == 0:
            if client.av_money < self.houses[0].cost:
                return None

        house = self.houses.pop(house_idx)

        if house.area > self.DISCOUNT_AREA:
            self.discount(house)

        # client
        client.av_money -= house.cost
        client.house = house

        # Steal your money with 10% chance
        self.av_money += house.cost * .1


if __name__ == '__main__':
    den = Person('Den', 25, av_money=70000, salary=3000)

    flat_cv1 = House(area=30, cost=40000)
    flat_cv2 = House(area=70, cost=90000)
    flat_cv3 = House(area=25, cost=30000)

    realtor = Realtor(name='David', age=50, av_money=1000000, salary=0, houses=[flat_cv1, flat_cv2, flat_cv3])
    realtor1 = Realtor(name='', age=0, av_money=0, salary=0, houses=[])

    # singleton tests
    assert realtor1.name == 'David'
    assert realtor is realtor1

    # tests of buying a house
    den.buy_a_house(realtor)
    assert den.has_home
    assert den.house is flat_cv1
