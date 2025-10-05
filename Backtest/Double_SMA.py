from backtesting import Backtest, Strategy
from backtesting.lib import crossover, plot_heatmaps

import talib

import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
import pandas as pd
import math

data = [
    "10Y/ADRO_10Y.csv",
    "10Y/AKRA_10Y.csv",
    "10Y/ASII_10Y.csv",
    "10Y/BBCA_10Y.csv",
    "10Y/BBNI_10Y.csv",
    "10Y/BBRI_10Y.csv",
    "10Y/BMRI_10Y.csv",
    "10Y/INCO_10Y.csv",
    "10Y/INDF_10Y.csv",
    "10Y/ITMG_10Y.csv",
    "10Y/MAPI_10Y.csv",
    "10Y/MEDC_10Y.csv",
    "10Y/PTBA_10Y.csv",
    "10Y/TLKM_10Y.csv",
    "10Y/UNTR_10Y.csv",
]

class DoubleSMAStrategy(Strategy): 

    allocation = 0.05 #5% 
    LOT_SIZE = 100 # 1 Lot = 100 shares

    short_length= 50
    long_length = 100

    def init(self): 
        self.short_sma = self.I(talib.SMA, self.data.Close.astype(float), self.short_length)
        self.long_sma = self.I(talib.SMA, self.data.Close.astype(float), self.long_length)

    def next(self): 

        numberOfLot = math.floor(self.equity * self.allocation / (round(self.data.Close[-1] * self.LOT_SIZE)))
        numberOfShares = numberOfLot * self.LOT_SIZE

        if crossover(self.long_sma, self.short_sma): 
            self.position.close()
        elif crossover(self.short_sma, self.long_sma) and numberOfLot > 0: 
            self.buy(size=numberOfShares)




optimization_results = []

def maximize_and_log(stats): 
    optimization_results.append({
        'Indicator Settings': "SMACross " + str(stats._strategy.short_length) + "," + str(stats._strategy.long_length),
        'Equity Final [Rp]': stats['Equity Final [$]'],
        'Return [%]': stats['Return [%]'],
        'Return Ann [%]': stats['Return (Ann.) [%]'],
        'Sharpe Ratio': stats['Sharpe Ratio'],
        'Sortino Ratio': stats['Sortino Ratio'],
        'Calmar Ratio': stats['Calmar Ratio'],
        'Max Drawdown [%]': stats['Max. Drawdown [%]'],
        'Max Drawdown Duration': stats['Max. Drawdown Duration'],
        'Total Trades': stats['# Trades'],
        'Win Rate [%]': stats['Win Rate [%]'],
        'Profit Factor': stats['Profit Factor'],
        'Avg Trade [%]': stats['Avg. Trade [%]'],
        'Best Trade [%]': stats['Best Trade [%]'],
        'Worst Trade [%]': stats['Worst Trade [%]']
    })
    print("SMAcross: " + str(len(optimization_results)))
    return stats['Sharpe Ratio']

# Plotting graph 
# stats = bt.run()
# print(stats)
# bt.plot()


counter = 0
for thing in data:
    optimization_results = []
    HISTORICAL_DATA= pd.read_csv(thing, parse_dates=['time'])
    HISTORICAL_DATA.set_index('time', inplace=True)
    bt = Backtest(HISTORICAL_DATA, DoubleSMAStrategy, cash = 100_000_000, trade_on_close=True)

    # OPTIMIZATION
    bestStats, heatmap = bt.optimize(
                short_length = range(5, 150, 1),
                long_length = range(50, 250, 1),
                maximize = maximize_and_log, 
                constraint = lambda param: param.long_length > param.short_length,
                #    max_tries = 100,
                return_heatmap=True
    )


    # plot_heatmaps(heatmap, agg='mean')

    results_df = pd.DataFrame(optimization_results)

    # Filtering out Curve-Fitting backtests & sort by Return [%]
    # filtered_df = results_df[
    #     (results_df['Win Rate [%]'] <= 90) &
    #     (results_df['Sharpe Ratio'] >= 0.3)
    # ]
    counter += 1
    sorted_df = results_df.sort_values(by="Return [%]", ascending=False)
    sorted_df.to_csv('./final_backtest/last/D_SMA-' + str(counter) + '.csv' , index=False)