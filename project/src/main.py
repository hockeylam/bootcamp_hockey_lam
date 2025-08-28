import os
import pandas as pd
import joblib
from load_data import get_data, flag_outliers_change
from strategy import geometric_dip_buyer
from backtest import run_backtest
from artifact import plot_strategy_and_spy_growth, plot_spy_with_SMA, plot_relative_performance, plot_predictions
from regression import run_linear_regression, run_prediction

df = get_data("SPY", interval="1d", lookback_days=500)

## feature engineering
df['change'] = df['close'].diff()
df['percent_change'] = (df['change'] / df['close'].shift(1))*100

##remove outliers
df = flag_outliers_change(df)
outlier_count = df['change_outlier'].sum()
print(df[df['change_outlier']])
print(f"Flagged {outlier_count} outliers")

#SMA
df['30_day_SMA'] = df['close'].rolling(30).mean().shift(1)
#Moving Volatility
df['30_day_volat'] = df['close'].rolling(30).std().shift(1)

#remove first 30 (invalid SMA and volatility calculations)
df = df.drop(df.index[:30]).copy()
df['days_sequence'] = range(1, len(df) + 1)

plot_spy_with_SMA(df)

pd.set_option('display.max_columns', None)
print(df.tail()['days_sequence'])

signals = geometric_dip_buyer(df, lookback_months=6, share_size=5, take_profit_pct=0.25)
results = run_backtest(df['close'], signals, starting_capital=100000)

plot_strategy_and_spy_growth(results, df['close'])
plot_relative_performance(results, df['close'])


features = ['open', 'days_sequence'] 

model, y_pred = run_linear_regression(df, features=features)
plot_predictions(df, y_pred, features=features)

model_dir = os.path.join(os.path.dirname(__file__), '..', 'model')
os.makedirs(model_dir, exist_ok=True)

model_path = os.path.join(model_dir, 'linear_model.pkl')
joblib.dump(model, model_path)


run_prediction(model, features=features, open_price=df['open'].iloc[-1], day_sequence=df['days_sequence'].iloc[-1] + 1)
