from typing import Tuple
import pandas as pd
import sklearn.preprocessing as pre
from typeguard import typechecked


@typechecked
def normalize_minmax(df: pd.DataFrame, minmax_scaler: pre.MinMaxScaler = None) -> Tuple[pd.DataFrame, pre.MinMaxScaler]:
    if minmax_scaler is None:
        minmax_scaler = pre.MinMaxScaler()
        data_norm = minmax_scaler.fit_transform(df.values)
    else:
        data_norm = minmax_scaler.transform(df.values)
    return pd.DataFrame(data=data_norm, index=df.index, columns=df.columns), minmax_scaler


@typechecked
def normalize_std(df: pd.DataFrame, std_scaler: pre.StandardScaler = None) -> Tuple[pd.DataFrame, pre.StandardScaler]:
    if std_scaler is None:
        std_scaler = pre.StandardScaler()
        data_norm = std_scaler.fit_transform(df.values)
    else:
        data_norm = std_scaler.transform(df.values)
    return pd.DataFrame(data=data_norm, index=df.index, columns=df.columns), std_scaler


@typechecked
def denormalize(df: pd.DataFrame, scaler) -> pd.DataFrame:
    data_denorm = scaler.inverse_transform(df.values)
    return pd.DataFrame(data=data_denorm, index=df.index, columns=df.columns)
