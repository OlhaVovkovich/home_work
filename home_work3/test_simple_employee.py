import requests
import unittest
from unittest.mock import patch


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


person1 = Employee('Seok-Jin', 'Kim', 100000)
person2 = Employee('Taehyung', 'Kim', 200000)


class TestEmployee(unittest.TestCase):

    def test_email(self):
        self.assertEqual(person1.email, 'Seok-Jin.Kim@email.com')
        self.assertEqual(person2.email, 'Taehyung.Kim@email.com')

    def test_fullname(self):
        person1.first = 'Nam-joon'
        person2.last = 'Vi'

        self.assertIsNot(person1.fullname, 'Seok-Jin Kim')
        self.assertEqual(person2.fullname, 'Taehyung Vi')

    def test_apply_raise(self):
        person1.apply_raise()
        self.assertEqual(person1.pay, 105000)
        person2.apply_raise()
        self.assertEqual(person2.pay, 210000)

    def test_monthly_schedule(self):
        with patch('requests.get') as mock:
            mock.return_value.ok = False
            mock.return_value.text = 'Done'

            person = Employee('Ji-min', 'Park', 1000000)
            schedule = person.monthly_schedule('June')
            mock.assert_called_with("http://company.com/Park/June")
            self.assertEqual(schedule, 'Bad Response!')


if __name__ == '__main__':
    unittest.main()
