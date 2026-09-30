import pandas as pd
import numpy as np


def smaCrossover(close: pd.Series, fast: int = 20, slow: int = 50) -> pd.Series:
    f, s = close.rolling(fast).mean(), close.rolling(slow).mean()
    return (f > s).astype(int).where(s.notna(), 0)


def monthlyMomentum(close: pd.Series, lookback: int = 1) -> pd.Series:

    month_ret = close.resample("ME").last().pct_change(lookback)
    return np.sign(month_ret).reindex(close.index, method="ffill").fillna(0)


STRATEGIES = {"SMA crossover": smaCrossover, "Monthly momentum": monthlyMomentum}
