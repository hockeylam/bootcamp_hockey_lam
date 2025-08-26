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

def plot_spy_with_SMA(df, title: str = "SPY Price vs 30-Day SMA"):
    """
    Plots SPY close price and 30-day SMA over time using datetime index.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['close'], label='Close', color='blue', linewidth=2)
    plt.plot(df.index, df['30_day_SMA'], label='30-Day SMA', color='orange', linewidth=2, linestyle='--')

    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_relative_performance(results: pd.DataFrame, prices: pd.Series):
    """
    Plots strategy % change minus SPY % change over time.
    """
    strategy_pct = results['Total Value'] / results['Total Value'].iloc[0] * 100
    spy_pct = prices / prices.iloc[0] * 100
    alpha_pct = strategy_pct - spy_pct

    plt.plot(alpha_pct.index, alpha_pct, label='Strategy - SPY', linewidth=1.5)
    plt.axhline(0, color='gray', linestyle='--', linewidth=1)
    plt.legend()
    plt.grid(True)
    plt.show()


from sklearn.model_selection import train_test_split

def plot_predictions(df: pd.DataFrame, y_pred, features: list, target: str = 'close', test_size: float = 0.2):
    """
    Minimal plot of predicted vs actual SPY close prices.
    """
    # Align predictions with test set
    X = df[features]
    y = df[target]
    _, X_test, _, y_test = train_test_split(X, y, test_size=test_size, shuffle=False)

    pred_series = pd.Series(y_pred, index=X_test.index)

    plt.plot(y_test.index, y_test.values, label='SPY Actual', color='black')
    plt.plot(pred_series.index, pred_series.values, label='Model Prediction', color='red')
    plt.legend()
    plt.show()
