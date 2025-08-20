import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from typing import List, Optional


def fill_missing_median(df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Fill NaNs in numeric columns (can be specified) with the median of each column.
    -------
    Returns pd.DataFrame
        A copy of the edited df with NaNs replaced by median values.
    """
    df_copy = df.copy()
    if columns is None:
        columns = df.select_dtypes(include=np.number).columns
    for col in columns:
        df_copy[col] = df_copy[col].fillna(df_copy[col].median())
    return df_copy


def drop_mostly_nan_cols(df: pd.DataFrame, threshold: Optional[float] = None ) -> pd.DataFrame:
    """
    Drop columns with more than 50% missing values. the threshold can be changed if stated

    Returns: pd.DataFrame
        A copy of the edited DataFrame with columns mostly NaNs removed.
    """
    if not threshold:
        threshold = len(df) * 0.5
    df_copy = df.dropna(axis=1, thresh=threshold)
    return df_copy


def drop_missing(df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Drop rows or columns based on missing values. 
    If columns is specified, then drop entries with nan on those columns.
    
    Returns: pd.DataFrame
        A copy of the edited DataFrame with rows or columns dropped.
    """
    df_copy = df.copy()
    if columns is not None:
        return df_copy.dropna(subset=columns)
    return df_copy.dropna()


def normalize_data(df: pd.DataFrame, columns: Optional[List[str]] = None, method: str = 'minmax') -> pd.DataFrame:
    """
    Scale numeric data using MinMaxScaler or StandardScaler.
    
    Returns: pd.DataFrame
        A copy of the DataFrame with scaled numeric columns.
    """
    df_copy = df.copy()
    if columns is None:
        columns = df_copy.select_dtypes(include=np.number).columns
    if method == 'minmax':
        scaler = MinMaxScaler()
    else:
        scaler = StandardScaler()
    df_copy[columns] = scaler.fit_transform(df_copy[columns])
    return df_copy


