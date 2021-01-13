import requests
import unittest
from unittest.mock import patch
from parameterized import parameterized_class


class Employee:
    """A sample Employee class"""

    raise_amt = 1.05

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay

    @property
    def email(self):
        return '{}.{}@email.com'.format(self.first, self.last)

    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amt)

    def monthly_schedule(self, month):
        response = requests.get(f"http://company.com/{self.last}/{month}")
        if response.ok:
            return response.text
        else:
            return 'Bad Response!'


@parameterized_class(('first', 'last', 'pay', 'email', 'fullname', 'up', 'res_ok', 'res_text', 'month', 'url'), [
    (
        'Seok-Jin',
        'Kim',
        100000,
        'Seok-Jin.Kim@email.com',
        'Seok-Jin Kim',
        105000,
        True,
        'Done',
        'June',
        'http://company.com/Kim/June'
    ),
    (
        'Taehyung',
        'Kim',
        200000,
        'Taehyung.Kim@email.com',
        'Taehyung Kim',
        210000,
        False,
        'Bad Response!',
        'July',
        'http://company.com/Kim/July'
    )
])
class TestEmployee(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.person = Employee(cls.first, cls.last, cls.pay)

    def test_email(self):
        self.assertEqual(self.person.email, self.email)

    def test_fullname(self):
        self.assertEqual(self.person.fullname, self.fullname)

    def test_apply_raise(self):
        self.person.apply_raise()
        self.assertEqual(self.person.pay, self.up)

    def test_monthly_schedule(self):
        with patch('requests.get') as mock:
            mock.return_value.ok = self.res_ok
            mock.return_value.text = self.res_text

            schedule = self.person.monthly_schedule(self.month)
            mock.assert_called_with(self.url)
            self.assertEqual(schedule, self.res_text)


if __name__ == '__main__':
    unittest.main()
