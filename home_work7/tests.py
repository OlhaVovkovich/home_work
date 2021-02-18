import unittest
import uuid

import crud

from datetime import datetime
from unittest import TestCase


class TestPositive(TestCase):

    def test_create_user(self):
        data = {
            'name': f'{uuid.uuid4()}',
            'email': f'{uuid.uuid4()}@{uuid.uuid4()}.com',
            'registration_time': datetime.now(),
        }

        id_us = crud.create_user(data)
        test_user = crud.read_user_info(id_us)
        self.assertEqual(data['name'], test_user['name'])


class TestNegative(TestCase):

    def test_create_user(self):
        with self.assertRaises(KeyError):
            crud.create_user({})


if __name__ == '__main__':
    unittest.main()
