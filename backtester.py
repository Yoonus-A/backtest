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
    asset = strategy_function(asset)

    return

def strategy_function(asset):
    """
    Dummy Trading strategy for testing :  Buy at the first trading day of the month
    Sell at the last trading day of the month
    """
    asset.index = pd.to_datetime(asset.index)

    months = asset.groupby([asset.index.year,asset.index.month])
    monthly_starts = months.head(1)
    monthly_ends = months.tail(1)

    start = monthly_starts.reset_index()
    end = monthly_ends.reset_index()

    start['year_month'] = start['Date'].dt.to_period('M')
    end['year_month'] = end['Date'].dt.to_period('M')

    monthly_trades = pd.merge(start[['year_month','Date','Close']],
                              end[['year_month','Date','Close']],
                              on='year_month', suffixes=('_start','_end')).drop(columns='year_month')
    print(monthly_trades)






    return asset
main()