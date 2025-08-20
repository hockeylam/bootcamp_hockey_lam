class BaseMarketData:
    def __init__(self, name):
        self.name = 'default'

    def get_timezone(self):
        raise NotImplementedError(f'NotImplementedError: instance name={self.name}')

    def get_regular_open(self):
        raise NotImplementedError(f'NotImplementedError: instance name={self.name}')

    def get_regular_close(self):
        raise NotImplementedError(f'NotImplementedError: instance name={self.name}')

    def get_early_close(self):
        raise NotImplementedError(f'NotImplementedError: instance name={self.name}')

    def get_special_market_close_days(self):
        raise NotImplementedError(f'NotImplementedError: instance name={self.name}')

    def get_special_early_close_days(self):
        raise NotImplementedError(f'NotImplementedError: instance name={self.name}')