from load_data import get_data
from strategy import geometric_dip_buyer
from backtest import run_backtest
from artifact import plot_strategy_and_spy_growth

df = get_data("SPY", interval="1d", lookback_days=500)

# feature engineering
df['change'] = df['close'].diff()
df['percent_change'] = (df['change'] / df['close'].shift(1))*100

signals = geometric_dip_buyer(df, lookback_months=6, share_size=5, take_profit_pct=0.25)
results = run_backtest(df['close'], signals, starting_capital=100000)

plot_strategy_and_spy_growth(results, df['close'])

