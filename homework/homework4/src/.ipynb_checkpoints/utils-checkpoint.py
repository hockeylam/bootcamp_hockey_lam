import pandas as pd
import requests
import datetime as dt

def validate_df(df, required_cols, dtypes_map):
    msgs = {}
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        msgs['missing_cols'] = f"Missing columns: {missing}"
    for col, dtype in dtypes_map.items():
        if col in df.columns:
            try:
                if dtype == 'datetime64[ns]':
                    pd.to_datetime(df[col])
                elif dtype == 'float':
                    pd.to_numeric(df[col])
            except Exception as e:
                msgs[f'dtype_{col}'] = f"Failed to coerce {col} to {dtype}: {e}"
    na_counts = df.isna().sum().sum()
    msgs['na_total'] = f"Total NA values: {na_counts}"
    return msgs

def alphavantage(SYMBOL,ALPHA_KEY):
    if ALPHA_KEY:
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": SYMBOL,
            "outputsize": "compact",
            "apikey": ALPHA_KEY,
            "datatype": "json"
        }
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        js = r.json()
        key = [k for k in js.keys() if "Time Series" in k]
        if not key:
            raise ValueError(f"Alpha Vantage response error: {js.get('Information', 'No time series data found.')}")
        series = js[key[0]]
        df_api = (pd.DataFrame(series).T
                  .rename_axis('date')
                  .reset_index())
        # keep a couple columns and coerce types
        df_api = df_api[['date', '4. close']].rename(columns={'4. close': 'adj_close'})
        df_api['date'] = pd.to_datetime(df_api['date'])
        df_api['adj_close'] = pd.to_numeric(df_api['adj_close'])
    else:
        import yfinance as yf
        df_api = yf.download(SYMBOL, period="6mo", interval="1d").reset_index()[['Date','Adj Close']]
        df_api.columns = ['date','adj_close']
    return df_api

def safe_stamp():
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")

def safe_filename(prefix, meta):
    mid = "_".join([f"{k}-{str(v).replace(' ', '-')[:20]}" for k, v in meta.items()])
    return f"{prefix}_{mid}_{safe_stamp()}.csv"
    