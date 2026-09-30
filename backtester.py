import sys
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

from strategies import STRATEGIES
from engine import run_backtest, metrics


def get_close(ticker: str, start: str, end: str) -> pd.Series:
    """Download adjusted close prices for one ticker."""
    data = yf.download(
        tickers=ticker,
        start=start,
        end=end,
        progress=False,
        multi_level_index=False,   # keeps 'Close' as a Series, not a DataFrame
    )
    if data.empty:
        raise ValueError(f"No data returned for '{ticker}'. Check the ticker and dates.")
    close = data["Close"].copy()
    close.index = pd.to_datetime(close.index)
    return close


def run(ticker, start, end, strategy_name, params=None, cost_bps=5):
    """Does the whole backtest and returns results"""
    params = params or {}
    close = get_close(ticker, start, end)
    position = STRATEGIES[strategy_name](close, **params)
    results = run_backtest(close, position, cost_bps=cost_bps)
    stats = pd.DataFrame({col: metrics(results[col]) for col in results.columns})
    return results, stats


def plot_cumulative_returns(results: pd.DataFrame, title: str = ""):
    """Plot c returns visualising return movements through set time"""
    cumulative = (1 + results).cumprod()
    plt.figure(figsize=(12, 6))
    plt.plot(cumulative["Asset"], label="Asset cumulative returns")
    plt.plot(cumulative["Strategy"], label="Strategy cumulative returns")
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Growth of 1")
    plt.grid(True)
    plt.legend()
    plt.show()


def main():
    ticker = "NFLX"
    strategy = "SMA crossover"          # or "Monthly momentum"
    params = {"fast": 20, "slow": 50}   # for monthly momentum: {"lookback": 1}

    results, stats = run(ticker, "2017-01-01", "2024-01-01", strategy, params, cost_bps=5)

    print(stats.round(4))
    plot_cumulative_returns(results, f"{ticker}: {strategy}")

if __name__ == "__main__":
    main()