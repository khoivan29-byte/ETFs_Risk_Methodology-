import os
import pandas as pd 
import yfinance as yf

# ETFs to track
tickers = ["SPY","QQQ","IWM","EFA","EEM","TLT","IEF","LQD","HYG","GLD","VNQ","DBC"]

# Download 5 years of daily data
data = yf.download(tickers, period="5y", interval="1d", auto_adjust=False)

# Keep adjusted close prices
prices = data["Adj Close"].dropna(how="all")

# Daily returns
returns = prices.pct_change().dropna(how="all")

# Save outputs
os.makedirs("data", exist_ok=True) 
prices.to_csv("data/prices.csv") 
returns.to_csv("data/returns.csv")

print("Done.")
print("Saved: data/prices.csv and data/returns.csv") 
print("Rows (days):", prices.shape[0], " | Columns (tickers):", prices.shape[1]) 