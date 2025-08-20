from IBridgePy.constants import MarketName
from market_calendar_factory.NoCalendar import NoCalendar
from market_calendar_factory.HasCalendar import HasCalendar


def get_marketCalendar(marketName):
    if marketName != MarketName.NONSTOP:
        return HasCalendar(marketName)
    else:
        return NoCalendar()
