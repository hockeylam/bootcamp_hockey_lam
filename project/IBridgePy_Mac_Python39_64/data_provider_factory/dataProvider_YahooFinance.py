# -*- coding: utf-8 -*-
"""
All rights reserved.
@author: IBridgePy@gmail.com
"""

import data_provider_factory.yfinance as yf
from IBridgePy.IbridgepyTools import calculate_startTime
from IBridgePy.constants import DataProviderName
from tools.hist_converter import convert_hist_using_datetime_to_epoch
from .data_provider_nonRandom import NonRandom
import pandas as pd


class YahooFinance(NonRandom):
    @property
    def name(self):
        return DataProviderName.YAHOO_FINANCE

    def provide_real_time_price(self, security, tickType):
        # Need to think about how to use this method
        raise NotImplementedError(f'NotImplementedError: instance name={self.name}')

    def provide_hist_from_a_true_dataProvider(self, security, endTime, goBack, barSize, whatToShow, useRTH):
        self._log.debug(__name__ + '::provide_hist_from_a_true_dataProvider: security=%s endTime=%s goBack=%s barSize=%s' % (security, endTime, goBack, barSize))
        startTime, endTime = calculate_startTime(endTime, goBack, barSize)
        # print(__name__ + '::provide_hist_from_a_true_dataProvider: startTime=%s endTime=%s' % (startTime, endTime))
        ticker = security.symbol
        hist_raw = yf.download(ticker, start=startTime)
        hist_ticker = _build_one(hist_raw, ticker)
        return convert_hist_using_datetime_to_epoch(hist_ticker)

    def ingest_hists(self, histIngestionPlan):
        # histIngestionPlan: data_provider_factor::data_loading_plan::HistIngestionPlan
        self._dataProviderClient.connectWrapper()
        self._ingest_hists(histIngestionPlan, self._get_hist_from_yahoo_finance)
        self._dataProviderClient.disconnectWrapper()
        self._histIngested = True

    def _get_hist_from_yahoo_finance(self, plan):
        self._log.debug(__name__ + '::_get_hist_from_yahoo_finance')
        # endTime = plan.endTime.astimezone(pytz.timezone('UTC'))
        # endTime = dt.datetime.strftime(endTime, "%Y%m%d %H:%M:%S %Z")  # datetime -> string
        ticker = plan.security.symbol
        hist_raw = yf.download(ticker, start='1990-01-01')
        hist_ticker = _build_one(hist_raw, ticker)
        return convert_hist_using_datetime_to_epoch(hist_ticker)


def _build_one(hist_raw, ticker):
    df_new = pd.DataFrame(index=hist_raw.index)
    df_new['open'] = hist_raw[('Open', ticker)]
    df_new['high'] = hist_raw[('High', ticker)]
    df_new['low'] = hist_raw[('Low', ticker)]
    df_new['close'] = hist_raw[('Close', ticker)]
    df_new['volume'] = hist_raw[('Volume', ticker)]
    return df_new
