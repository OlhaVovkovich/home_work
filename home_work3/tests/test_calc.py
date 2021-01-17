import unittest
from ..funcs.simple_calc import *
from parameterized import parameterized_class


@parameterized_class(('x', 'y', 'sum', 'sub', 'mul', 'div'), [
    (1, 1, 2, 0, 1, 1),
    (1.5, 0.5, 2, 1, 0.75, 3),
    (10, -10, 0, 20, -100, -1),
    (-10, -10, -20, 0, 100, 1),
    (1, 0, 1, 1, 0, 'ValueError'),
])
class Test(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(add(self.x, self.y), self.sum)

    def test_sub(self):
        self.assertEqual(subtract(self.x, self.y), self.sub)

    def test_mul(self):
        self.assertEqual(multiply(self.x, self.y), self.mul)

    def test_div(self):
        if self.y:
            self.assertEqual(divide(self.x, self.y), self.div)
        else:
            with self.assertRaises(ValueError):
                divide(self.x, self.y)


if __name__ == '__main__':
    unittest.main()