import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


def main():
    asset = yf.download(
        tickers = "AAPL",
        start = "2017-01-01",
        end = "2018-01-01",
        progress = False
    )
    # print(asset)
    asset = asset.reset_index()

    asset = strategy_function(asset)
    return

def strategy_function(asset):
    """
    Dummy Trading strategy for testing :  Buy at the start of the month
    Sell at the end of the month
    """
    Start = pd.Timestamp(year=2017, month=1, day=1)
    buy_sell_df = pd.DataFrame({
        "Start": pd.date_range(Start, periods=12, freq="MS"),
        "End": pd.date_range(Start, periods=12, freq="M")
    })
    print(buy_sell_df)
    return asset
main()