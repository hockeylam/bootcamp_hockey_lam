class MarketCalendarBase:

    @property
    def name(self):
        raise NotImplementedError(f'NotImplementedError: instance name={self.name}')

    # override
    def isTradingDay(self, aDatetime):
        raise NotImplementedError(f'NotImplementedError: instance name={self.name}')

    def is_market_open_at_this_moment(self, aDatetime):
        raise NotImplementedError(f'NotImplementedError: instance name={self.name}')

    def isEarlyClose(self, aDatetime):
        raise NotImplementedError(f'NotImplementedError: instance name={self.name}')






