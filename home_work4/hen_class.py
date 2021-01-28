import datetime
import requests


class ErrorTimesOfYear(Exception):
    pass


class HenHouse:
    min_hens_accepted = 5
    hens_productivity = {'winter': 0.25, 'spring': 0.75, 'autumn': 0.5, 'summer': 1}

    def __init__(self, hen_count: int):
        self.hen_count = hen_count
        if self.hen_count < self.min_hens_accepted:
            raise ValueError('You need more hens))')
        else:
            print("You have enough hens!!!")

    @property
    def season(self) -> str:
        month = {1: "winter",
                 2: "winter",
                 3: "spring",
                 4: "spring",
                 5: "spring",
                 6: "summer",
                 7: "summer",
                 8: "summer",
                 9: "autumn",
                 10: "autumn",
                 11: "autumn",
                 12: "winter",
                 }
        return month.get(datetime.datetime.today().month)

    def _productivity_index(self):
        if self.season in self.hens_productivity:
            return self.hens_productivity[self.season]
        raise ErrorTimesOfYear

    def get_eggs_daily(self, hen_count: int) -> int:
        return int(hen_count * self._productivity_index())

    def get_max_count_for_soup(self, expected_eggs: int) -> int:
        # based on hen_count self and get_eggs_daily we need to count hew many hens we can kill
        # but still get expected_eggs count of eggs
        if self.hen_count < self.min_hens_accepted \
                or self.get_eggs_daily(self.hen_count) < expected_eggs:
            return 0
        else:
            return int((self.get_eggs_daily(self.hen_count) - expected_eggs)
                       / self.hens_productivity[self.season])

    @staticmethod
    def food_price() -> int:
        page = requests.get("http:/chicken/food")

        if page.status_code == 200:
            return int(page.text[10])
        else:
            raise ConnectionError()
