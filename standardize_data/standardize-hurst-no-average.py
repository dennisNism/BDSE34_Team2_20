import os

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler

# 读取分群对照表
tech_clusterID_df = pd.read_csv('hurst_clustering_result_Technology.csv')
finance_clusterID_df = pd.read_csv('hurst_clustering_result_Finance.csv')
QQQ = pd.read_csv('C:/Share/期末專題/daily_data_combine/QQQ.csv', index_col='Date', parse_dates=['Date'])
QQQ.sort_index(inplace = True)
XLF = pd.read_csv('C:/Share/期末專題/daily_data_combine/XLF.csv', index_col='Date', parse_dates=['Date'])
XLF.sort_index(inplace = True)


# 创建一个空的字典来存储每个分群的DataFrame
tech_clusterID = {i: pd.DataFrame() for i in range(0,5)}
finance_clusterID = {i: pd.DataFrame() for i in range(0,5)}

# 设定时间范围
start_date = '2024-01-02'
end_date = '2024-06-20'

# 读取科技股数据并进行处理
tech_folder = 'C:/Share/期末專題/tech_index_signal/stock_data_model_new/Technology_new'  # 替换为实际的文件夹路径
for _, row in tech_clusterID_df.iterrows():
    symbol = row['stockID']
    clusterID = row['clusterID']  # 分组信息
    filepath = os.path.join(tech_folder, f"{symbol}.csv")
    if os.path.exists(filepath):
        df = pd.read_csv(filepath, index_col='Date', parse_dates=['Date'])
        df = df.loc[start_date:end_date]
        # 标准化 Adj Close
        scaler = StandardScaler()
        df['Adj Close'] = scaler.fit_transform(df[['Adj Close']])
        tech_clusterID[clusterID][symbol] = df['Adj Close']

# 读取财金股数据并进行处理
finance_folder = 'C:/Share/期末專題/tech_index_signal/stock_data_model_new/Finance_new'  # 替换为实际的文件夹路径
for _, row in finance_clusterID_df.iterrows():
    symbol = row['stockID']
    clusterID = row['clusterID']  # 分组信息
    filepath = os.path.join(finance_folder, f"{symbol}.csv")
    if os.path.exists(filepath):
        df = pd.read_csv(filepath, index_col='Date', parse_dates=['Date'])
        df = df.loc[start_date:end_date]
        # 标准化 Adj Close
        scaler = StandardScaler()
        df['Adj Close'] = scaler.fit_transform(df[['Adj Close']])
        finance_clusterID[clusterID][symbol] = df['Adj Close']

# QQQ & XLF 標準化
QQQ = QQQ.loc[start_date:end_date]
XLF = XLF.loc[start_date:end_date]

scaler = StandardScaler()
QQQ['Price'] = scaler.fit_transform(QQQ[['Price']])
XLF['Price'] = scaler.fit_transform(XLF[['Price']])


# 计算分群的加总平均值并绘制趋势图
clusterID_to_plot = [0, 1, 2, 3, 4]  # 指定要绘制的group
for clusterID, data in tech_clusterID.items():
    if clusterID in clusterID_to_plot and not data.empty:
        for symbol in data.columns:
            plt.figure(figsize=(14, 7))
            plt.plot(data.index, data[symbol], label=f'{symbol}')
            plt.title(f'Technology hurst clusterID {clusterID} - {symbol} Adj Close')
            plt.xlabel('Date')
            plt.ylabel('Standardized Adj Close')
            plt.legend()
            plt.savefig(f'pic/tech_hurst_cluster_{clusterID}/{symbol}.png', format='png')
            plt.close()
        
clusterID_to_plot = [0, 1, 2, 3, 4]  # 指定要绘制的group
for clusterID, data in finance_clusterID.items():
    if clusterID in clusterID_to_plot and not data.empty:
        for symbol in data.columns:
            plt.figure(figsize=(14, 7))
            plt.plot(data.index, data[symbol], label=f'{symbol}')
            plt.title(f'Finance hurst clusterID {clusterID} - {symbol} Adj Close')
            plt.xlabel('Date')
            plt.ylabel('Standardized Adj Close')
            plt.legend()
            plt.savefig(f'pic/fin_hurst_cluster_{clusterID}/{symbol}.png', format='png')
            plt.close()
