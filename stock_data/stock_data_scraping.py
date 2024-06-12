#import package
import yfinance as yf
import os
import csv

# Path of stock symbols
path = 'stock_tickers.txt'
# Path of data
data_dir = 'stock_data'
# File to stock symbol and df_len
output_file = 'ticker_lengths.csv'

# Make a directory
os.makedirs(data_dir, exist_ok=True)

# Download data
with open(path, 'r') as f, open(output_file, 'w', newline='') as csvfile:
    lines = f.readlines()
    writer = csv.writer(csvfile)
    writer.writerow(['Ticker', 'Data Length', 'First Date', 'Last Date'])  # Write header
    for line in lines:
        ticker = line.strip("\n")
        print(f'Processing {ticker}...')
        try:
            df = yf.download(ticker, start='1984-06-01', end='2024-05-31')
            df_len = len(df)
            if df.empty:
                print(f'{ticker} has no data available.')
                writer.writerow([Symbol, 'No data available', '', ''])
                continue
            df.to_csv(os.path.join(data_dir, ticker + '.csv'))
            first_date = df.index[0].strftime('%Y-%m-%d') 
            last_date = df.index[-1].strftime('%Y-%m-%d') 
            writer.writerow([Symbol, df_len, first_date, last_date])
            print(f'Data for {ticker} saved successfully.')
            print(df_len)
        except Exception as e:
            print(f'Error processing {ticker}: {e}')
            writer.writerow([Symbol, f'Error: {e}', '' , ''])
            continue