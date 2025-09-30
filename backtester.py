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