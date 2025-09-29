import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from strategies import smaCrossover, monthlyMomentum


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

    asset['Returns'] = asset['Close'].pct_change() # asset daily returns
    strat_data = monthlyMomentum(asset)
    strat_data = calculate_returns(strat_data)
    calculateMetrics(asset, strat_data)
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

    # calculate positions to take
    monthly_trades['Position'] = np.where(
        monthly_trades['Close_end'] > monthly_trades['Close_start'], 1,
        np.where(monthly_trades['Close_end'] < monthly_trades['Close_start'], -1, 0)
    )
    return monthly_trades


def calculateMetrics(asset_data, strat_data):
    rfr = 0.04 # annual risk-free rate
    d_rfr = rfr / len(strat_data['Position'].dropna().values) # daily rfr
    mean_strategy_returns = np.mean(strat_data['Strategy Returns'].dropna().values)
    std_dev = np.std(strat_data['Strategy Returns'])
    sharpe_ratio = ((mean_strategy_returns - d_rfr) / std_dev) * np.sqrt(len(strat_data['Position'].dropna().values))
    volatility = strat_data['Returns'].dropna().std() * np.sqrt(len(strat_data['Position'].dropna().values))

    mean_returns = np.mean(asset_data['Returns'].dropna().values)
    std_dev_asset = np.std(asset_data['Returns'])
    asset_sharpe_ratio = ((mean_returns - (rfr / 252)) / std_dev_asset) * np.sqrt(252)
    asset_volatility = std_dev_asset * np.sqrt(252)

    print(f"Strategy Returns sharpe ratio: {sharpe_ratio}")
    print(f"Strategy Volatility: {volatility}")
    print(" ")
    print(f"Asset Returns sharpe ratio: {asset_sharpe_ratio}")
    print(f"Asset Volatility: {asset_volatility}")




def calculate_returns(df):

    if 'Returns' not in df.columns:
        df['Returns'] = df['Close'].pct_change() # calculate returns if the column does not exist
    #print(df['Returns'])
    df['Strategy Returns'] = df['Returns'].dropna() * df['Position'].shift(1) # calculate strategy returns
    #print(df['Close'])
    #print(df['Position'])
    #print(df['Strategy Returns'])
    return df

# Plot cumulative returns of asset vs. strategy
def plot_cumulative_returns(strat_data,asset):
    strat_data_creturns = (1+strat_data['Strategy Returns']).cumprod()
    asset_creturns = (1+asset['Returns']).cumprod()

    plt.figure(figsize=(12,6))
    plt.plot(asset_creturns, label = 'Asset cumulative returns')
    plt.plot(strat_data_creturns, label='Strategy cumulative returns')
    plt.xlabel('Dates')
    plt.ylabel('Cumulative returns')
    plt.grid(True)
    plt.legend()
    plt.show()
    return
main()