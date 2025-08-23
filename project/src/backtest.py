import pandas as pd

def run_backtest(prices: pd.Series, signals: list[int], starting_capital: float = 10000):
    """
    Executes trades based on signals and tracks portfolio performance.
    Buys and sells as much as it can if the signal is too great.
    returns: pd.DataFrame: Portfolio history with columns:
        ['Price','Shares','Cash','Position Value','Total Value']
    """
    cash = starting_capital
    shares = 0
    history = []

    for i in range(len(prices)):
        price = prices.iloc[i]
        signal = signals[i]
        
        if signal > 0:
            max_affordable = int(cash // price)
            qty = min(signal, max_affordable)
            cost = qty * price
            cash -= cost
            shares += qty
        elif signal < 0:
            qty = min(abs(signal), shares)
            revenue = qty * price
            cash += revenue
            shares -= qty

        position_value = shares * price
        total_value = cash + position_value

        history.append({
            'Price': price,
            'Shares': shares,
            'Cash': cash,
            'Position Value': position_value,
            'Total Value': total_value
        })

    return pd.DataFrame(history, index=prices.index)
