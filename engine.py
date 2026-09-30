import numpy as np
import pandas as pd

def run_backtest(close: pd.Series, position: pd.Series, cost_bps: float = 5) -> pd.DataFrame:
    ret = close.pct_change()
    pos = position.shift(1).fillna(0)                 # trade on the next bar: no look-ahead
    turnover = pos.diff().abs().fillna(0)
    strat = pos * ret - turnover * cost_bps / 10_000
    return pd.DataFrame({"Asset": ret, "Strategy": strat}).dropna()

def metrics(r: pd.Series, periods: int = 252, rfr: float = 0.04) -> dict:
    eq = (1 + r).cumprod()
    years = len(r) / periods
    sd = r.std()
    return {
        "CAGR": eq.iloc[-1] ** (1 / years) - 1,
        "Volatility": sd * np.sqrt(periods),
        "Sharpe": (r.mean() - rfr / periods) / sd * np.sqrt(periods),
        "Max drawdown": (eq / eq.cummax() - 1).min(),
    }