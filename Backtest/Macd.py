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


class MACDStrategy(Strategy): 

    allocation = 0.05 #5% 
    LOT_SIZE = 100 # 1 Lot = 100 shares

    fast_period = 12
    slow_period = 26
    signal_period = 150

    def init(self): 
        self.macd, self.signal, self.histogram = self.I(
            talib.MACD,
            self.data.Close.astype(float),
            self.fast_period,
            self.slow_period,
            self.signal_period
        )

    def next(self): 

        numberOfLot = math.floor(self.equity * self.allocation / (round(self.data.Close[-1] * self.LOT_SIZE)))
        numberOfShares = numberOfLot * self.LOT_SIZE

        if crossover(self.signal, self.macd) and self.macd > 0: 
            self.position.close()
        elif crossover(self.macd, self.signal) and self.macd < 0 and numberOfLot > 0: 
            self.buy(size=numberOfShares)


optimization_results = []

def maximize_and_log(stats): 
    optimization_results.append({
        'Indicator Settings': "MACD " + str(stats._strategy.fast_period) + "," + str(stats._strategy.slow_period) + "," + str(stats._strategy.signal_period),
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
    print("MACD: " + str(len(optimization_results)))
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
    bt = Backtest(HISTORICAL_DATA, MACDStrategy, cash = 100_000_000, trade_on_close=True)


    # OPTIMIZATION
    bestStats, heatmap = bt.optimize(
                    fast_period = range(5, 20, 1),
                    slow_period = range(21, 36, 1),
                    signal_period = range(5, 200, 1),
                maximize = maximize_and_log, 
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
    sorted_df.to_csv('./final_backtest/last/MACD-' + str(counter) + '.csv' , index=False)