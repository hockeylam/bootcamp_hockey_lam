import sys
import yfinance as yf
import pandas as pd

def get_data(ticker: str, interval: str = '1d', lookback_days: int = 756) -> pd.DataFrame:
    """
    Loads historical market data using yfinance.
    ticker (str): Stock or ETF symbol (e.g., 'SPY')
    interval (str): Data interval ('1d', '1h', '1m', etc.)
    lookback_days (int): Number of trading days to retrieve (capped at 7 if interval is one minute)

    Returns: pd.DataFrame: DataFrame downloaded from yfinance
    """
    # Convert lookback_days to period string
    if interval in ['1d', '1h']:
        period = str(lookback_days)+"d"
    elif interval == '1m':
        period = "7d"  # yfinance
    else:
        raise ValueError("Unsupported interval for free data")

    df = yf.download(ticker, period=period, interval=interval, progress=False)
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

    # Clean and standardize
    df = df.dropna()
    df = df.rename(columns=str.lower)
    df.index.name = 'datetime'

    return df


#def print_data_summary(df):
#    print("\n=== Data Summary ===")
#   print(f"Rows: {len(df)}")
#    print(f"Columns: {list(df.columns)}")
#    print("\nHead:")
#    print(df.head())

#df = get_data("SPY","1d",756)
#print_data_summary(df)
