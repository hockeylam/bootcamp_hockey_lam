# -*- coding: utf-8 -*-
"""
@author: IBridgePy@gmail.com
All rights reserved.
"""
from .MarketCalendarBase import MarketCalendarBase


class NoCalendar(MarketCalendarBase):
    @property
    def name(self):
        return 'NoCalendar'

    def isTradingDay(self, timeNow):
        return True

    def is_market_open_at_this_moment(self, aDatetime):
        return True

    def isEarlyClose(self, aDatetime):
        raise False
