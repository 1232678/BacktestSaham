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


class StochasticStrategy(Strategy): 

    allocation = 0.05 #5% 
    LOT_SIZE = 100 # 1 Lot = 100 shares

    k_period = 22
    d_period = 5
    d_smoothing = 6
    lower_bound = 31
    upper_bound= 87

    def init(self): 
        self.k, self.d = self.I(talib.STOCH, self.data.High.astype(float), self.data.Low.astype(float), self.data.Close.astype(float), self.k_period, self.d_period, self.d_smoothing)
        # self.short_sma = self.I(talib.SMA, self.data.Close.astype(float), self.short_length)

    def next(self): 

        numberOfLot = math.floor(self.equity * self.allocation / (round(self.data.Close[-1] * self.LOT_SIZE)))
        numberOfShares = numberOfLot * self.LOT_SIZE

        if crossover(self.d, self.k) and self.k > self.upper_bound: 
            self.position.close()
        elif crossover(self.k, self.d) and self.k < self.lower_bound and numberOfLot > 0: 
            self.buy(size=numberOfShares)




optimization_results = []

def maximize_and_log(stats): 
    optimization_results.append({
        'Indicator Settings': "STO " + str(stats['_strategy'].k_period) + "," + 
        str(stats['_strategy'].d_period) + "," + 
        str(stats['_strategy'].d_smoothing) + " " + "(" + 
        str(stats['_strategy'].upper_bound) + "," + 
        str(stats['_strategy'].lower_bound)+ ")",
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
    print("Stoch: " + str(len(optimization_results)))
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
    bt = Backtest(HISTORICAL_DATA, StochasticStrategy, cash = 100_000_000, trade_on_close=True)


    # OPTIMIZATION
    bestStats, heatmap = bt.optimize(
                    k_period = range(10, 40, 2),
                    d_period = range(5, 20, 1),
                    d_smoothing = range(2, 7, 1),
                    lower_bound = range(10, 40, 2),
                    upper_bound= range(60, 90, 2),
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
    sorted_df.to_csv('./final_backtest/last/STO-' + str(counter) + '.csv' , index=False)