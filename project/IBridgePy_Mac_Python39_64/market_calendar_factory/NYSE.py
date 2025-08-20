import datetime as dt

import pytz

from .BaseMarketData import BaseMarketData


class NYSE(BaseMarketData):
    def __init__(self):
        BaseMarketData.__init__(self, 'NYSE')

    def get_timezone(self):
        return pytz.timezone('EDT')

    def get_regular_open(self):
        return 9 * 60 + 30  # EDT 9:30 AM

    def get_regular_close(self):
        return 16 * 60  # EDT 16:00

    def get_early_close(self):
        return 13 * 60  # EDT 13:00

    def get_special_market_close_days(self):
        return [
            dt.date(2023, 1, 2),dt.date(2024, 1, 1),dt.date(2025, 1, 1),
            dt.date(2023, 1, 16),dt.date(2024, 1, 15),dt.date(2025, 1, 20),
            dt.date(2023, 2, 20),dt.date(2024, 2, 19),dt.date(2025, 2, 17),
            dt.date(2023, 4, 7),dt.date(2024, 3, 29),dt.date(2025, 4, 18),
            dt.date(2023, 5, 29),dt.date(2024, 5, 27),dt.date(2025, 5, 26),
            dt.date(2023, 6, 19),dt.date(2024, 6, 19),dt.date(2025, 6, 19),
            dt.date(2023, 7, 4),dt.date(2024, 7, 4),dt.date(2025, 7, 4),
            dt.date(2023, 9, 4),dt.date(2024, 9, 2),dt.date(2025, 9, 1),
            dt.date(2023, 11, 23),dt.date(2024, 11, 28),dt.date(2025, 11, 27),
            dt.date(2023, 12, 25), dt.date(2024, 12, 25), dt.date(2025, 12, 25)
        ]

    def get_special_early_close_days(self):
        return [dt.date(2023, 7, 3),dt.date(2024, 7, 3),dt.date(2025, 7, 3),
                dt.date(2023, 11, 24),dt.date(2024, 11, 29),dt.date(2025, 11, 28),
                                                       dt.date(2024, 12, 24),dt.date(2025, 12, 24)
               ]
