import numpy as np
import pandas as pd

stock = pd.read_csv('AAPL.csv', index_col="Date", parse_dates=True)

stock['RSI14_over_heat'] = stock['RSI14'] > 70
stock['RSI14_over_cold'] = stock['RSI14'] < 30

stock['Close > SMA5'] = stock['Close'] > stock['Close_SMA5']
stock['STD > 1.5'] = stock['Close'] .rolling(10).std() > 1.5

# 黃金交叉
def crossover(over,down):
    a1 = over
    b1 = down
    a2 = a1.shift(1)
    b2 = b1.shift(1)
    crossover =  (a1>a2) & (a1>b1) & (b2>a2)
    return crossover
# 死亡交叉
def crossunder(down,over):
    a1 = down
    b1 = over
    a2 = a1.shift(1)
    b2 = b1.shift(1)
    crossdown =  (a1<a2) & (a1<b1) & (b2<a2)
    return crossdown

stock['KD_Golden_Cross'] = crossover(stock['Stochastic_K'],stock['Stochastic_D'])
stock['KD_Death_Cross'] = crossunder(stock['Stochastic_K'],stock['Stochastic_D'])

low_range_kd = 25 # KD值低檔通常設定於20-30之間
stock['Low_Range_D'] = stock['Stochastic_D'] < 25

stock['Buy_In'] = (stock['KD_Golden_Cross'] & stock['Low_Range_D'])
stock['Sold_Out'] = stock['KD_Death_Cross']

stock['MACD_Golden_Cross']=(stock['DIF']>stock['MACD']) & (stock['DIF'].shift(1)<stock['MACD'].shift(1))
stock['MACD_Death_Cross']=(stock['DIF']<stock['MACD']) & (stock['DIF'].shift(1)>stock['MACD'].shift(1))

stock.to_csv('AAPL(new).csv')