# -*- coding: utf-8 -*-
"""
@author: IBridgePy@gmail.com
All rights reserved.
"""
from BasicPyLib.BasicTools import convert_datetime_to_date
from .MarketCalendarBase import MarketCalendarBase
from sys import exit


def convert_datetime_to_hour_minute(a_datetime):
    hour = a_datetime.hour
    minute = a_datetime.minute
    return hour * 60 + minute


class HasCalendar(MarketCalendarBase):
    def __init__(self, calendar_name):
        self.calendar_name = calendar_name
        self.not_trading_days = []
        self.early_close_days = []
        self.regular_open = None
        self.regular_close = None
        self.early_close = None
        self._load_true_calendar()

    @property
    def name(self):
        return self.calendar_name

    def _load_true_calendar(self):
        if self.calendar_name == 'NYSE':
            from .NYSE import NYSE
            nyse = NYSE()
            self.not_trading_days = nyse.get_special_market_close_days()
            self.early_close_days = nyse.get_special_early_close_days()
            self.regular_open = nyse.get_regular_open()
            self.regular_close = nyse.get_regular_close()
            self.early_close = nyse.get_early_close()
        else:
            exit(f'Cannot handle calendar_name={self.calendar_name}')
        assert len(self.not_trading_days) != 0
        assert type(self.regular_open) == int
        assert type(self.regular_close) == int
        assert type(self.early_close) == int
        assert type(self.early_close_days) == list
        assert type(self.not_trading_days) == list

    def isTradingDay(self, timeNow):
        a_date = convert_datetime_to_date(timeNow)
        if a_date in self.not_trading_days:
            return False
        if 0 <= a_date.weekday() <= 4:  # Monday = 0, Friday = 4
            return True
        else:
            return False

    def is_market_open_at_this_moment(self, aDatetime):
        if not self.isTradingDay(aDatetime):
            return False
        hour_minute = convert_datetime_to_hour_minute(aDatetime)
        if self.isEarlyClose(aDatetime):
            return self.regular_open <= hour_minute < self.early_close
        else:
            return self.regular_open <= hour_minute < self.regular_close

    def isEarlyClose(self, aDatetime):
        a_date = convert_datetime_to_date(aDatetime)
        return a_date in self.early_close_days
