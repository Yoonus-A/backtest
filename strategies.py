import pandas as pd
import numpy as np


def smaCrossover(asset):
    """
    Moving avg crossover strategy
    """
    asset.index = pd.to_datetime(asset.index)

    asset['SMA20'] = asset['Close'].rolling(window=20).mean()
    asset['SMA50'] = asset['Close'].rolling(window=50).mean()

    asset['Position'] = np.where(asset['SMA20'] > asset['SMA50'], 1,-1)
    asset['Position'] = asset['Position'].replace(to_replace=0, method='ffill')
    return asset

def monthlyMomentum(asset):

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

    # single df holding buy and sell points data
    monthly_trades = pd.merge(start[['year_month','Date','Close']],
                              end[['year_month','Date','Close']],
                              on='year_month', suffixes=('_start','_end')).drop(columns='year_month')

    # index trades by date makes comparisons with asset simpler
    monthly_trades.set_index('Date_end', inplace=True)

    # calculate positions to take
    monthly_trades['Position'] = np.where(
        monthly_trades['Close_end'] > monthly_trades['Close_start'], 1,
        np.where(monthly_trades['Close_end'] < monthly_trades['Close_start'], -1, 0)
    )
    monthly_trades = monthly_trades.rename(columns={'Close_end': 'Close'}) # rename close column to make calculations consistent
    return monthly_trades

