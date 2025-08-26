import pandas as pd
import numpy as np

def geometric_dip_buyer(df, lookback_months=6, share_size=1, take_profit_pct=0.10):
    """
    Returns a list of daily trade signals based on drawdown from rolling high.
    """
    df = df.copy()
    window = lookback_months * 21
    df['high'] = df['close'].rolling(window=window, min_periods=1).max()

    signals = []
    position = 0
    invested = 0.0

    for i in range(len(df)):
        price = df['close'].iloc[i]
        high = df['high'].iloc[i]
        drawdown_percent = (high - price) / high

        if drawdown_percent >= 0.01:
            level = int(drawdown_percent * 100)
            qty = 2 ** (level - 1) * share_size
            signals.append(qty)
            position += qty
            invested += qty * price
        else:
            signals.append(0)

        if position > 0:
            market_value = position * price
            open_pl = market_value - invested
            if open_pl / invested >= take_profit_pct:
                signals[-1] = -position 
                position = 0
                invested = 0.0

    return signals

def linear_dip_buyer(df, lookback_months=6, share_size=1, take_profit_pct=0.10):
    """
    Returns a list of daily trade signals based on drawdown from rolling high.
    """
    df = df.copy()
    window = lookback_months * 21
    df['high'] = df['close'].rolling(window=window, min_periods=1).max()

    signals = []
    position = 0
    invested = 0.0

    for i in range(len(df)):
        price = df['close'].iloc[i]
        high = df['high'].iloc[i]
        drawdown_percent = (high - price) / high

        if drawdown_percent >= 0.01:
            level = int(drawdown_percent * 100)
            qty = level * share_size
            signals.append(qty)
            position += qty
            invested += qty * price
        else:
            signals.append(0)

        if position > 0:
            market_value = position * price
            open_pl = market_value - invested
            if open_pl / invested >= take_profit_pct:
                signals[-1] = -position 
                position = 0
                invested = 0.0

    return signals

def SMA_crossover_30(df, share_size=10000):
    """
    Returns a list of daily trade signals based on price crossing the 30-day SMA.
    Buys when price crosses above SMA, sells when it crosses below
    """
    df = df.copy()

    signals = []
    for i in range(len(df)):
        if i == 0:
            signals.append(0)
            continue

        prev_close = df['close'].iloc[i - 1]
        prev_sma = df['30_day_SMA'].iloc[i - 1]
        curr_close = df['close'].iloc[i]
        curr_sma = df['30_day_SMA'].iloc[i]

        if np.isnan(prev_sma) or np.isnan(curr_sma):
            signals.append(0)
            continue

        # Buy signal: crossed above
        if prev_close < prev_sma and curr_close > curr_sma:
            signals.append(share_size)
        # Sell signal: crossed below
        elif prev_close > prev_sma and curr_close < curr_sma:
            signals.append(-share_size)
        else:
            signals.append(0)

    return signals
