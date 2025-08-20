#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
There is a risk of loss when trading stocks, futures, forex, options and other
financial instruments. Please trade with capital you can afford to
lose. Past performance is not necessarily indicative of future results.
Nothing in this computer program/code is intended to be a recommendation, explicitly or implicitly, and/or
solicitation to buy or sell any stocks or futures or options or any securities/financial instruments.
All information and computer programs provided here is for education and
entertainment purpose only; accuracy and thoroughness cannot be guaranteed.
Readers/users are solely responsible for how to use these information and
are solely responsible any consequences of using these information.

If you have any questions, please send email to IBridgePy@gmail.com
All rights reserved.
"""

import bisect
import datetime as dt
import os
import subprocess
from copy import copy
from sys import exit
from decimal import Decimal

import pandas as pd
import pytz

from BasicPyLib.BasicTools import get_system_info
from Config.base_settings import PROJECT, BROKER_CLIENT
# noinspection PyUnresolvedReferences
from IBridgePy import IBCpp
from IBridgePy.OrderTypes import OrderStyle
from IBridgePy.constants import SymbolStatus, ExchangeName
from IBridgePy.quantopian import Security, from_security_to_contract, from_contract_to_security
from broker_client_factory.BrokerClientDefs import ReqHistParam
from models.Order import IbridgePyOrder

barSizeToSecondMap = {'1 sec': 1,
                      '5 secs': 5,
                      '15 secs': 15,
                      '30 secs': 30,
                      '1 min': 60,
                      '2 mins': 120,
                      '3 mins': 180,
                      '5 mins': 300,
                      '15 mins': 900,
                      '30 mins': 1800,
                      '1 hour': 3600,
                      '1 day': 86400}
ibGoBardLetterToSecondsMap = {
    'S': 1,
    'D': 86400,
    'W': 86400 * 5,
    'M': 86400 * 23,
    'Y': 86400 * 252
}


def calculate_startTime(endTime, goBack, barSize):
    endTime = adjust_endTime(endTime, barSize)
    startTime = None
    if 'S' in goBack:
        startTime = endTime - dt.timedelta(seconds=int(goBack[:-1]) + 2 * 24 * 60 * 60)  # +2 to handle weekend issue
    elif 'D' in goBack:
        startTime = endTime - dt.timedelta(days=int(goBack[:-1]) + 2)  # +2 to handle weekend issue
    elif 'W' in goBack:
        startTime = endTime - dt.timedelta(weeks=int(goBack[:-1]))
    elif 'M' in goBack:
        startTime = endTime - dt.timedelta(days=int(goBack[:-1]) * 30)
    elif 'Y' in goBack:
        startTime = endTime.replace(endTime.year - int(goBack[:-1]))
    return startTime, endTime


def convert_goBack_barSize(goBack, barSize):
    # print(__name__ + '::convert_goBack_barSize: goBack=%s barSize=%s' % (goBack, barSize))
    return int(int(goBack[:-2]) * ibGoBardLetterToSecondsMap[goBack[-1:]] / barSizeToSecondMap[barSize])


def adjust_endTime(endTime, barSize):
    # !!!!strptime silently discard tzinfo!!!
    if type(endTime) is str:
        endTime = dt.datetime.strptime(endTime, "%Y%m%d %H:%M:%S %Z")  # string -> dt.datetime
        endTime = pytz.timezone('UTC').localize(endTime)
    if barSize == '1 second':
        endTime = endTime.replace(microsecond=0)
    elif barSize == ReqHistParam.BarSize.ONE_MIN:
        endTime = endTime.replace(second=0, microsecond=0)
    elif barSize in ['1 hour', '4 hours']:
        endTime = endTime.replace(minute=0, second=0, microsecond=0)
    elif barSize == '1 day':
        endTime = endTime.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        endTime = endTime.replace(second=0, microsecond=0)
    return endTime


def symbol(str_security):
    """
    IBridgePy::Trader has self.symbol that will be used by IBridgePy users.
    This symbol will be used by other purposes.
    For example, symbol in the following line
    histIngestionPlan.add(Plan(security=symbol('SPY'), barSize='1 min', fileName='xxx.csv'))
    :param str_security:
    :return:
    """
    security = from_symbol_to_security(str_security)
    # return add_exchange_primaryExchange_to_security(security)
    return security


def symbols(*args):
    ans = []
    for item in args:
        ans.append(symbol(item))
    return ans


def from_symbol_to_security(s1):
    if ',' not in s1:
        s1 = 'STK,%s,USD' % (s1,)

    secType = s1.split(',')[0].strip()
    ticker = s1.split(',')[1].strip()
    currency = s1.split(',')[2].strip()
    if secType in ['CASH', 'STK']:
        return Security(secType=secType, symbol=ticker, currency=currency)
    else:
        print('Definition of %s is not clear!' % (s1,))
        print('Please use superSymbol to define a str_security')
        print(r'http://www.ibridgepy.com/ibridgepy-documentation/#superSymbol')
        exit()


def from_string_to_security(st):
    if ',' not in st:
        print(__name__ + '::from_string_to_security: EXIT, format is not correct')
        exit()
    stList = st.split(',')
    secType = stList[0].strip()
    if secType in ['CASH', 'STK']:
        primaryExchange = stList[1].strip()
        exchange = stList[2].strip()
        ticker = stList[3].strip()
        currency = stList[4].strip()
        return Security(secType=secType, symbol=ticker, currency=currency, exchange=exchange,
                        primaryExchange=primaryExchange, symbolStatus=SymbolStatus.STRING_CONVERTED)

    elif secType in ['FUT', 'BOND']:
        primaryExchange = stList[1].strip()
        exchange = stList[2].strip()
        ticker = stList[3].strip()
        currency = stList[4].strip()
        expiry = stList[5].strip()
        return Security(secType=secType, symbol=ticker, currency=currency, exchange=exchange,
                        primaryExchange=primaryExchange, expiry=expiry,
                        symbolStatus=SymbolStatus.STRING_CONVERTED)
    else:
        primaryExchange = stList[1].strip()
        exchange = stList[2].strip()
        ticker = stList[3].strip()
        currency = stList[4].strip()
        expiry = stList[5].strip()
        strike = float(stList[6].strip())
        right = stList[7].strip()
        multiplier = stList[8].strip()
        return Security(secType=secType, symbol=ticker, currency=currency, exchange=exchange,
                        primaryExchange=primaryExchange, expiry=expiry, strike=strike, right=right,
                        multiplier=multiplier,
                        symbolStatus=SymbolStatus.STRING_CONVERTED)


# noinspection PyShadowingNames
def superSymbol(secType=None,
                symbol=None,
                currency='USD',
                exchange='',
                primaryExchange='',
                localSymbol='',
                tradingClass='',
                expiry='',
                strike=0.0,
                right='',
                multiplier='',
                includeExpired=False,
                conId=None,
                comboLegDirection=None,
                comboLegRatio=None
                ):
    if not isinstance(strike, float):
        print(__name__ + '::superSymbol: EXIT, strike must be a float!')
        exit()
    if not isinstance(expiry, str):
        print(__name__ + '::superSymbol: EXIT, expiry must be a string!')
        exit()
    if not isinstance(localSymbol, str):
        print(__name__ + '::superSymbol: EXIT, localSymbol must be a string!')
        exit()
    if not isinstance(multiplier, str):
        print(__name__ + '::superSymbol: EXIT, multiplier must be a string!')
        exit()
    if secType in ['FUT', 'OPT']:
        if len(expiry) not in [6, 8]:
            raise Exception(f'ERROR: expiry of {secType} is neither 6 nor 8')
    return Security(secType=secType, symbol=symbol, currency=currency, exchange=exchange, localSymbol=localSymbol, tradingClass=tradingClass,
                    primaryExchange=primaryExchange, expiry=expiry, strike=strike, right=right,
                    multiplier=multiplier, includeExpired=includeExpired, symbolStatus=SymbolStatus.SUPER_SYMBOL,
                    conId=conId, comboLegDirection=comboLegDirection, comboLegRatio=comboLegRatio)


def read_in_hash_config(fileName):
    full_file_path = os.path.join(os.getcwd(), 'IBridgePy', fileName)
    return read_hash_config(full_file_path)


def read_hash_config(full_file_path):
    if os.path.isfile(full_file_path):
        with open(full_file_path) as f:
            line = f.readlines()
        return line[0].strip()
    else:
        print('hash.conf file is missing at %s. EXIT' % (str(full_file_path),))
        exit()


def special_match(target, val, version):
    # print(__name__ + '::special_match: target=%s val=%s version=%s' % (target, val, version))
    if target == 'any':
        return True
    else:
        if version == 'monthWeek':
            if target >= 0:
                return target == val[0]
            else:
                return target == val[1]
        elif version == 'hourMinute':
            return target == val
        else:
            print(__name__ + '::_match: EXIT, cannot handle version=%s' % (version,))
            exit()


def display_all_contractDetails(contractDetails):
    for item in ['conId', 'symbol', 'secType', 'LastTradeDateOrContractMonth',
                 'strike', 'right', 'multiplier', 'exchange', 'currency',
                 'localSymbol', 'primaryExchange', 'tradingClass',
                 'includeExpired', 'secIdType', 'secId', 'comboLegs', 'underComp',
                 'comboLegsDescrip']:
        try:
            print(item, getattr(contractDetails.summary, item))
        except AttributeError:
            print(item, 'not found')
    for item in ['marketName', 'minTick', 'priceMagnifier', 'orderTypes',
                 'validExchanges', 'underConId', 'longName', 'contractMonth',
                 'industry', 'category', 'subcategory',
                 'timeZoneId', 'tradingHours', 'liquidHours',
                 'evRule', 'evMultiplier', 'mdSizeMultiplier', 'aggGroup',
                 'secIdList',
                 'underSymbol', 'underSecType', 'marketRuleIds', 'realExpirationDate',
                 'cusip', 'ratings', 'descAppend',
                 'bondType', 'couponType', 'callable', 'putable',
                 'coupon', 'convertible', 'maturity', 'issueDate',
                 'nextOptionDate', 'nextOptionType', 'nextOptionPartial',
                 'notes']:
        try:
            print(item, getattr(contractDetails, item))
        except AttributeError:
            print(item, 'not found in contractDetails')


def create_order(orderId, accountCode, security, amount, orderDetails, createdTime,
                 ocaGroup=None, ocaType=None, transmit=None, parentId=None,
                 orderRef='', outsideRth=False, hidden=False):
    contract = from_security_to_contract(security)
    if not isinstance(amount, Decimal):
        amount = Decimal(amount)

    order = {}
    if hidden:
        if contract.exchange == ExchangeName.ISLAND:
            order['hidden'] = True
        else:
            print(__name__ + '::create_order: EXIT, only ISLAND accept hidden orders')
            exit()

    if amount > 0:
        order['action'] = 'BUY'
    elif amount < 0:
        order['action'] = 'SELL'

    order['orderId'] = orderId
    order['account'] = accountCode
    order['totalQuantity'] = str(abs(amount))  # decimal to str
    order['orderType'] = orderDetails.orderType  # LMT, MKT, STP

    order['orderRef'] = str(orderRef)
    order['outsideRth'] = outsideRth

    if orderDetails.tif is not None:
        order['tif'] = orderDetails.tif

    if ocaGroup is not None:
        order['ocaGroup'] = ocaGroup
    if ocaType is not None:
        order['ocaType'] = ocaType
    if transmit is not None:
        order['transmit'] = transmit
    if parentId is not None:
        order['parentId'] = parentId

    if orderDetails.orderType in ['MKT', 'MOC']:
        pass
    elif orderDetails.orderType == 'LMT':
        order['lmtPrice'] = orderDetails.limit_price
    elif orderDetails.orderType == 'STP':
        order['auxPrice'] = orderDetails.stop_price
    elif orderDetails.orderType == 'STP LMT':
        order['lmtPrice'] = orderDetails.limit_price
        order['auxPrice'] = orderDetails.stop_price
    elif orderDetails.orderType == 'TRAIL LIMIT':
        if orderDetails.trailing_amount is not None:
            order['auxPrice'] = orderDetails.trailing_amount  # trailing amount
        if orderDetails.trailing_percent is not None:
            order['trailingPercent'] = orderDetails.trailing_percent
        order['trailStopPrice'] = orderDetails.stop_price
        if order['action'] == 'SELL':
            order['lmtPrice'] = orderDetails.stop_price - orderDetails.limit_offset
        elif order['action'] == 'BUY':
            order['lmtPrice'] = orderDetails.stop_price + orderDetails.limit_offset
    elif orderDetails.orderType == 'TRAIL':
        if orderDetails.trailing_amount is not None:
            order['auxPrice'] = orderDetails.trailing_amount  # trailing amount
        if orderDetails.trailing_percent is not None:
            order['trailingPercent'] = orderDetails.trailing_percent
        if orderDetails.stop_price is not None:
            order['trailStopPrice'] = orderDetails.stop_price
    else:
        print(__name__ + '::create_order: EXIT,Cannot handle orderType=%s' % (orderDetails.orderType,))

    # From IB TWS 983+, a few new errorCodes are added and they are not backward compatible.
    # errorCode=10268 errorMessage=The 'EtradeOnly' order attribute is not supported.
    # TerrorCode=10269 errorMessage=The 'firmQuoteOnly' order attribute is not supported
    order['eTradeOnly'] = False
    order['firmQuoteOnly'] = False
    an_order = IbridgePyOrder(requestedContract=contract, requestedOrder=order, createdTime=createdTime)
    return an_order


def stripe_exchange_primaryExchange_from_contract(contract):
    security = from_contract_to_security(contract)
    return stripe_exchange_primaryExchange_from_security(security)


def stripe_exchange_primaryExchange_from_security(security):
    copy_security = copy(security)
    copy_security.exchange = ''
    copy_security.primaryExchange = ''
    return copy_security


def check_same_security(sec1, sec2):
    if sec1.secType in ['STK', 'CASH']:
        items = ['secType', 'symbol', 'currency']
    elif sec1.secType == 'FUT':
        items = ['secType', 'symbol', 'currency', 'expiry']
    else:
        items = ['secType', 'symbol', 'currency', 'expiry', 'strike',
                 'right', 'multiplier']
    for para in items:
        if getattr(sec1, para) != getattr(sec2, para):
            return False
    return True


def extract_contractDetails(df, field):
    ans = {}
    if type(field) == str:
        field = [field]
    for item in field:
        if item in ['conId', 'symbol', 'secType', 'LastTradeDateOrContractMonth', 'strike', 'right', 'multiplier',
                    'exchange', 'currency', 'localSymbol', 'primaryExchange', 'tradingClass', 'includeExpired',
                    'secIdType', 'secId', 'comboLegs', 'underComp', 'comboLegsDescrip']:
            if len(df) > 1:
                values = set([getattr(x.contract, item) for x in df['contractDetails']])
                if len(values) > 1:
                    ans[item] = f'many contracts ({len(df)}) have different {item}. The values are {values}'
                    continue
                else:
                    ans[item] = list(values)[0]
            if hasattr(df.iloc[0]['contractDetails'].contract, item):
                ans[item] = getattr(df.iloc[0]['contractDetails'].contract, item)
            else:
                ans[item] = 'not found'
        elif item in ['marketName', 'minTick', 'priceMagnifier', 'orderTypes', 'validExchanges', 'underConId',
                      'longName', 'contractMonth', 'industry', 'category', 'subcategory', 'timeZoneId',
                      'tradingHours', 'liquidHours', 'evRule', 'evMultiplier', 'mdSizeMultiplier', 'aggGroup',
                      'secIdList', 'underSymbol', 'underSecType', 'marketRuleIds', 'realExpirationDate', 'cusip',
                      'ratings', 'descAppend', 'bondType', 'couponType', 'callable', 'putable', 'coupon',
                      'convertible', 'maturity', 'issueDate', 'nextOptionDate', 'nextOptionType',
                      'nextOptionPartial', 'notes']:
            if len(df) > 1:
                values = set([getattr(x, item) for x in df['contractDetails']])
                if len(values) > 1:
                    ans[item] = f'many contracts ({len(df)}) have different {item}. The values are {values}'
                    continue
                else:
                    ans[item] = ans[item] = list(values)[0]
            if hasattr(df.iloc[0]['contractDetails'], item):
                ans[item] = getattr(df.iloc[0]['contractDetails'], item)
            else:
                ans[item] = 'not found'
        elif item == 'summary':
            return df.loc[:, ['security']]
            # return df.loc[:, ['contractName', 'expiry', 'strike', 'right', 'multiplier', 'contract', 'security']]
        else:
            print(__name__ + '::_extract_contractDetails: Invalid item = %s' % (item,))
            exit()
    return ans


def choose_whatToShow(secType):
    if secType in ['STK', 'FUT', 'IND', 'BOND']:
        return 'TRADES'
    elif secType in ['CASH', 'OPT', 'CFD', 'CONTFUT']:
        return 'ASK'
    else:
        print(__name__ + '::request_historical_data: EXIT, security.secType=%s must specify whatToShow.' % (secType,))
        exit()


def print_decisions(decisions):
    """

    :param decisions: a dict key = security object, value = int number of shares to buy or sell
    :return: str rep of decisions.
    """
    if not decisions:
        return 'Empty decision'
    ans = ''
    for security in decisions:
        ans += '%s:%s\n' % (security, decisions[security])
    return ans


def convert_market_hours_to_df(hoursString):
    """
    Convert market hours that are returned from get_contract_details to pd.DataFrame
    :param hoursString: market hours that are returned from get_contract_details
    :return: pd.DataFrame, columns=['open', 'close'] int=hour * 60 + minute; index=datetime.date
    """

    def convert_one_day_hour_string(x):
        """
        Input looks like this, returned from get_contract_details
        20200724:0930-20200724:1600
        20200725:CLOSED
        """
        ans = {}
        if '-' in x:
            x1 = x.split('-')
            a, b = x1[0].split(':')
            ans['date'] = dt.datetime.strptime(a, "%Y%m%d")  # string -> dt.datetime
            ans['open'] = int(b[:2]) * 60 + int(b[2:])
            tt = x1[1].split(':')[1]
            ans['close'] = int(tt[:2]) * 60 + int(tt[2:])
        else:
            a, b = x.split(':')
            ans['date'] = dt.datetime.strptime(a, "%Y%m%d")  # string -> dt.datetime
            ans['open'] = b
            ans['close'] = b
        return ans

    v = map(convert_one_day_hour_string, hoursString.split(';'))
    dd = pd.DataFrame(v, columns=['date', 'open', 'close'])
    dd = dd.set_index('date')
    return dd


def filter_options_by_closest_expiry(df, dt_targetExpiry):
    if not isinstance(dt_targetExpiry, dt.datetime):
        raise Exception('type(dt_targetExpiry) must be datetime.datetime.')
    df['expiry_diff'] = df['security'].apply(lambda x: (dt.datetime.strptime(x.expiry, "%Y%m%d") - dt_targetExpiry).days)
    sorted_exp = sorted(list(set(df['expiry_diff'])))
    loc = bisect.bisect_left(sorted_exp, -1)
    if loc >= len(sorted_exp):
        loc = -1
    return df[df['expiry_diff'] == sorted_exp[loc]]


def filter_options_by_expiry_range(df, dt_startExpiry_inclusive, dt_endExpiry_inclusive):
    if isinstance(dt_startExpiry_inclusive, dt.datetime):
        dt_startExpiry_inclusive = dt_startExpiry_inclusive.date()
    if isinstance(dt_endExpiry_inclusive, dt.datetime):
        dt_endExpiry_inclusive = dt_endExpiry_inclusive.date()
    if not isinstance(dt_startExpiry_inclusive, dt.date):
        raise Exception('type(dt_startExpiry_inclusive) must be datetime.date')
    if not isinstance(dt_endExpiry_inclusive, dt.date):
        raise Exception('type(dt_endExpiry_inclusive) must be datetime.date')
    df['expiry_diff'] = df['security'].apply(lambda x: dt.datetime.strptime(x.expiry, "%Y%m%d").date())
    return df[(df['expiry_diff'] <= dt_endExpiry_inclusive) & (df['expiry_diff'] >= dt_startExpiry_inclusive)]


def filter_options_by_strike_range(df, lower_strike_inclusive, upper_strike_inclusive):
    df['strike'] = df['security'].apply(lambda x: float(x.strike))
    return df[(df['strike'] <= upper_strike_inclusive) & (df['strike'] >= lower_strike_inclusive)]


def filter_options_by_closest_strike(dff, targetStrike):
    # A value is trying to be set on a copy of a slice from a DataFrame.
    # Try using .loc[row_indexer,col_indexer] = value instead
    df = dff.copy()  # To avoid the above error, make a copy of incoming dff
    df['strike_diff'] = df['security'].apply(lambda x: x.strike - float(targetStrike))
    sorted_exp = sorted(list(set(df['strike_diff'])))
    loc = bisect.bisect_left(sorted_exp, 0)
    if loc >= len(sorted_exp):
        loc = -1
    return df.loc[df['strike_diff'] == sorted_exp[loc], :]


def read_and_parse_identity_file():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'IBridgePy', 'identity.csv')
    df_identity = pd.read_csv(file_path, header=0, index_col=0)
    ans = {}
    for key in df_identity.index:
        ans[key.strip()] = str(df_identity.loc[key]['value']).strip()
    return ans


def check_user_sys_compatibility():
    # print('check system compatibility')
    # Check if IBridgePy package matches user's environment.
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'IBridgePy', 'identity.csv')
    platform, pythonName, pythonVersion = get_system_info()
    info = read_and_parse_identity_file()
    ibpySys = info['sys']
    ibpyPython = info['python']
    ibpyVersion = info['version']
    if str(ibpySys) != str(platform) or str(ibpyPython) != str(pythonName) or int(ibpyVersion) != int(pythonVersion):
        print('The environment is "%s %s %s"' % (platform, pythonName, pythonVersion))
        print('IBridgePy package is for "%s %s %s"' % (ibpySys, ibpyPython, ibpyVersion))
        print("They don't match!")
        print('Please visit https://ibridgepy.com/download/ and download the correct IBridgePy package for %s %s %s' % (ibpySys, ibpyPython, ibpyVersion))
        exit()
    if 'startup' not in info:
        with open(file_path, 'a') as f:
            f.write('\nstartup, False')
        if bool(info.get('docker', False)):
            update_docker_ip()


def update_docker_ip():
    # print('update_docker_ip')
    PATH = os.path.join(os.path.join(PROJECT['rootFolderPath'], 'settings.py'))
    if BROKER_CLIENT['IB_CLIENT'].get('host', None):
        # print('host is there')
        return

    ip = find_ip()
    if not ip:
        # print('Did not find docker ip')
        return

    with open(PATH) as f:
        lines = f.readlines()

    i = 0
    for i in range(len(lines)):
        if "'IB_CLIENT': {" == lines[i].strip():
            break
    if i:
        lines = lines[:i + 1] + [f"        'host': '{ip}',\n"] + lines[i + 1:]
        with open(PATH, 'w') as f:
            f.write(''.join(lines))
            # print('written to setting.py')


def find_docker_ip(cmd):
    result = subprocess.getoutput(cmd)
    ans = None
    for ln in result.split('\n'):
        if 'prvt.dyno.rt.heroku.com' in ln or 'host.docker.internal' in ln:
            ans = ln.split(' ')[0]
            break
    return ans


def find_ip():
    ip = find_docker_ip('getent ahosts')
    if not ip:
        ip = find_docker_ip('getent ahosts host.docker.internal')
    return ip


def create_combo_contract(securities):
    contract = {'symbol': securities[0].symbol,
                'secType': 'BAG',
                'currency': securities[0].currency,
                'exchange': securities[0].exchange,
                'comboLegs': []}
    for security in securities:
        leg = {'conId': security.conId,
               'ratio': int(security.comboLegRatio),
               'action': security.comboLegDirection,
               'exchange': security.exchange}
        contract['comboLegs'].append(leg)
    return contract


def build_combo_order(int_orderId, adj_accountCode, securities, amount, comboDirection, orderStyle: OrderStyle, outsideRth, createdTime):
    order = _prepare_order(int_orderId, adj_accountCode, amount, comboDirection, orderStyle, outsideRth)
    contract = create_combo_contract(securities)
    return IbridgePyOrder(requestedContract=contract, requestedOrder=order, createdTime=createdTime)


def _prepare_order(orderId, accountCode, amount, direction, orderStyle: OrderStyle, outsideRth):
    if not isinstance(amount, Decimal):
        amount = Decimal(amount)

    order = {}
    order['action'] = direction
    order['orderId'] = orderId
    order['account'] = accountCode
    order['totalQuantity'] = str(abs(amount))  # decimal to str
    order['orderType'] = orderStyle.orderType  # LMT, MKT, STP
    order['tif'] = orderStyle.tif
    order['outsideRth'] = outsideRth

    if orderStyle.orderType in ['MKT', 'MOC']:
        pass
    elif orderStyle.orderType == 'LMT':
        order['lmtPrice'] = orderStyle.limit_price
    elif orderStyle.orderType == 'STP':
        order['auxPrice'] = orderStyle.stop_price
    elif orderStyle.orderType == 'STP LMT':
        order['lmtPrice'] = orderStyle.limit_price
        order['auxPrice'] = orderStyle.stop_price
    elif orderStyle.orderType == 'TRAIL LIMIT':
        if orderStyle.trailing_amount is not None:
            order['auxPrice'] = orderStyle.trailing_amount  # trailing amount
        if orderStyle.trailing_percent is not None:
            order['trailingPercent'] = orderStyle.trailing_percent
        order['trailStopPrice'] = orderStyle.stop_price
        if order['action'] == 'SELL':
            order['lmtPrice'] = orderStyle.stop_price - orderStyle.limit_offset
        elif order['action'] == 'BUY':
            order['lmtPrice'] = orderStyle.stop_price + orderStyle.limit_offset
    elif orderStyle.orderType == 'TRAIL':
        if orderStyle.trailing_amount is not None:
            order['auxPrice'] = orderStyle.trailing_amount  # trailing amount
        if orderStyle.trailing_percent is not None:
            order['trailingPercent'] = orderStyle.trailing_percent
        if orderStyle.stop_price is not None:
            order['trailStopPrice'] = orderStyle.stop_price
    else:
        exit(f'EXIT,Cannot handle orderType={orderStyle.orderType}')

    # From IB TWS 983+, a few new errorCodes are added and they are not backward compatible.
    # errorCode=10268 errorMessage=The 'EtradeOnly' order attribute is not supported.
    # TerrorCode=10269 errorMessage=The 'firmQuoteOnly' order attribute is not supported
    order['eTradeOnly'] = False
    order['firmQuoteOnly'] = False
    return order


if __name__ == '__main__':
    read_and_parse_identity_file()

