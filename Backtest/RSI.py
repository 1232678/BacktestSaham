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



class RsiStrategy(Strategy): 

    allocation = 0.05 # 5% 
    LOT_SIZE = 100 # 1 Lot = 100 shares

    upper_bound = 92
    lower_bound = 56
    length = 5

    def init(self): 
        self.rsi = self.I(talib.RSI, self.data.Close.astype(float), self.length)

    def next(self): 

        numberOfLot = math.floor(self.equity * self.allocation / (round(self.data.Close[-1] * self.LOT_SIZE)))
        numberOfShares = numberOfLot * self.LOT_SIZE

        # benchmark performance composite
        # if self.position.is_long: 
        #     pass
        # else: 
        #     self.buy()

        if crossover(self.upper_bound, self.rsi): 
            self.position.close()
        elif crossover(self.rsi, self.lower_bound) and numberOfLot > 0: 
            self.buy(size=numberOfShares)


optimization_results = []

def maximize_and_log(stats): 
    optimization_results.append({
        'Indicator Settings': "RSI " + str(stats._strategy.length) + "," + str(stats._strategy.lower_bound) + "," + str(stats._strategy.upper_bound),
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
    print('RSI: ' + str(len(optimization_results)))
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
    bt = Backtest(HISTORICAL_DATA, RsiStrategy, cash = 100_000_000, trade_on_close=True)

    # OPTIMIZATION
    bestStats, heatmap = bt.optimize(
                upper_bound = range(55, 95, 1),
                lower_bound = range(10, 45, 1),
                length = range(5, 40, 1),
                maximize = maximize_and_log,
                constraint = lambda param: param.upper_bound > param.lower_bound,
                # max_tries = 100,
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
    sorted_df.to_csv('./final_backtest/last/RSI-' + str(counter) + '.csv' , index=False)