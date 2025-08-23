import matplotlib.pyplot as plt
import pandas as pd

def plot_strategy_and_spy_growth(results: pd.DataFrame, prices: pd.Series, title: str = "Strategy vs SPY Performance"):
    """
    Plots % change of strategy vs % change of SPY over time.
    returns: None
    """
    # Normalize both series to start at 100
    strategy_pct = results['Total Value'] / results['Total Value'].iloc[0] * 100
    spy_pct = prices / prices.iloc[0] * 100

    plt.figure(figsize=(12, 6))
    plt.plot(strategy_pct.index, strategy_pct - 100, label='Strategy % Change', linewidth=2)
    plt.plot(spy_pct.index, spy_pct - 100, label='SPY % Change', linewidth=2, linestyle='--')

    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Cumulative % Change")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
