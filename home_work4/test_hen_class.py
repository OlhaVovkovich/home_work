import unittest
from unittest.mock import patch, PropertyMock

from parameterized import parameterized

from hen_class import HenHouse, ErrorTimesOfYear


class TestHenHouse(unittest.TestCase):

    def setUp(self) -> None:
        # optional method, may be used to initialize hen_house instance
        self.hh = HenHouse(hen_count=5)

    def test_init_with_equal_min(self):
        hh = HenHouse(hen_count=5)
        self.assertEqual(hh.hen_count, 5)

    def test_init_with_less_than_min(self):
        with self.assertRaises(ValueError):
            HenHouse(hen_count=0)

    @parameterized.expand([
        (1, 'winter'),
        (4, 'spring'),
        (7, 'summer'),
        (10, 'autumn'),
    ])
    def test_season(self, month, season):
        # mock the datetime method/attribute which returns month number
        # make sure correct month ("winter"/"spring" etc.) is returned from season method
        # try to return different seasons

        with patch('datetime.datetime') as dt_mock:
            dt_mock.today.return_value.month = month
            self.assertEqual(self.hh.season, season)

    def test_productivity_index(self):
        # mock the season method return with some correct season
        # make sure _productivity_index returns correct value based on season and HenHouse.hens_productivity attribute
        with patch('hen_class.HenHouse.season', new_callable=PropertyMock) as season_mock:
            season_mock.return_value = 'summer'
            hh = HenHouse(hen_count=5)
            self.assertEqual(hh._productivity_index(), 1)

    def test_productivity_index_incorrect_season(self):
        # mock the season method return with some incorrect season
        # make sure ErrorTimesOfYear is raised when _productivity_index called
        with patch('hen_class.HenHouse.season', new_callable=PropertyMock) as season_mock:
            season_mock.return_value = 'fall'
            hh = HenHouse(hen_count=5)
            with self.assertRaises(ErrorTimesOfYear):
                hh._productivity_index()

    @patch('hen_class.HenHouse._productivity_index', return_value=.25)
    def test_get_eggs_daily_in_winter(self, _):
        # test get_eggs_daily function
        # _productivity_index method or season should be mocked
        hh = HenHouse(hen_count=5)
        self.assertEqual(hh.get_eggs_daily(8), 2)

    def test_get_max_count_for_soup(self):
        # call get_max_count_for_soup with expected_eggs number and check that correct number is returned

        # Note: make sure to mock _productivity_index or season
        # in order not to call datetime.datetime.today().month, since it is going to be dynamic value in the future
        with patch('hen_class.HenHouse.season', new_callable=PropertyMock) as season_mock:
            season_mock.return_value = 'summer'
            hh = HenHouse(hen_count=100)
            self.assertEqual(hh.get_max_count_for_soup(expected_eggs=80), 20)

    def test_get_max_count_for_soup_returns_zero(self):
        # call get_max_count_for_soup with expected_eggs number bigger than get_eggs_daily(self.hen_count)
        # zero should be returned.

        # Note: make sure to mock _productivity_index or season
        # in order not to call datetime.datetime.today().month, since it is going to be dynamic value in the future
        with patch('hen_class.HenHouse.season', new_callable=PropertyMock) as season_mock:
            season_mock.return_value = 'winter'
            hh = HenHouse(hen_count=100)
            self.assertEqual(hh.get_max_count_for_soup(expected_eggs=80), 0)

    def test_food_price(self):
        # mock requests.get and make the result has status_code attr 200 and text to some needed value
        # make sure food-price() return will be of int type
        with patch('requests.get') as requests_get_mock:
            requests_get_mock.return_value.status_code = 200
            requests_get_mock.return_value.text = '00000000001'

            self.assertEqual(HenHouse.food_price(), 1)

    def test_food_price_connection_error(self):
        # mock requests.get and make the result has status_code attr not 200
        # check that ConnectionError is raised when food_price method called
        with patch('requests.get') as requests_get_mock:
            requests_get_mock.return_value.status_code = 500
            with self.assertRaises(ConnectionError):
                HenHouse.food_price()


if __name__ == '__main__':
    unittest.main()
