import unittest
from ..funcs.simple_employee import *
from unittest.mock import patch
from parameterized import parameterized_class


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
