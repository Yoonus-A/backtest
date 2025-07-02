import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


def main():

    """
    runs backtest by getting stock data and applying strategy to it
    :return:
    """
    asset = yf.download(
        tickers = "AAPL",
        start = "2017-01-01",
        end = "2018-01-01",
        progress = False
    )
    asset['Returns'] = asset['Close'].pct_change()
    asset_ret = (asset['Close'].loc['2017-12-29','AAPL'] - asset['Close'].loc['2017-01-03','AAPL']) / asset['Close'].loc['2017-01-03','AAPL']
    strat_data = strategy_function(asset)
    strat_data['Returns'] = calculate_returns(strat_data)
    plot_cumulative_returns(strat_data, asset)
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

    # single df holding buy and sell points data
    monthly_trades = pd.merge(start[['year_month','Date','Close']],
                              end[['year_month','Date','Close']],
                              on='year_month', suffixes=('_start','_end')).drop(columns='year_month')

    # index trades by date makes comparisons with asset simpler
    monthly_trades.set_index('Date_end', inplace=True)
    return monthly_trades


def calculate_returns(df):
    return (df['Close_end'] - df['Close_start']) / df['Close_start']


# Plot cumulative returns of asset vs. strategy
def plot_cumulative_returns(strat_data,asset):
    strat_data_creturns = (1+strat_data['Returns']).cumprod()
    asset_creturns = (1+asset['Returns']).cumprod()
    # print(asset_creturns)
    # print(strat_data)
    # print(asset)

    return


main()