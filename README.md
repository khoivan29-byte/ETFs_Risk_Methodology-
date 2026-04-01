# The file in this branch, risk_metrics.py, transforms market return data into portfolio performance analytics. It builds the equal-weight ETF portfolio, computes performance and downside-risk measures, and generates the metric outputs used in the final Excel dashboard.

The script performs the main portfolio analytics tasks:

1. The script imports the cleaned ETF return dataset (a CSV file in this case). It loads the data into a pandas DataFrame, with dates as the time index and ETF tickers as columns.
2. The script finds the dates that exist in both datasets and keeps only the shared date range. This ensures that prices and returns stay synchronized before any calculations are performed.
3. The list of tickers is taken directly from the columns of the return file. This makes the script flexible as long as the return file is structured correctly.
4. The script includes two main helper functions:
    Maximum drawdown function:
        Builds an equity curve from a return series, tracks the running peak, and returns the worst drawdown as a negative number.
    Historical VaR/CVaR function
        Uses the return distribution to calculate historical VaR and CVaR at the chosen confidence level. These are returned as positive loss magnitudes.
5. For each ETF, the script calculates:
    Annualized volatility
    Maximum drawdown
    Historical VaR95
    Historical CVaR95
    Correlation with SPY
    First valid date
    Last valid date
    Number of observations.
These results are stored in a summary table indexed by ticker.
7. The script then creates an equal-weight portfolio by assigning the same weight to every ETF in the return table. It  computes the portfolio return series and stores it as: PORT_EQW. 
8. For the equal-weight portfolio, the script calculates the same headline metrics as for each ETF:
    Annualized volatility
    Aaximum drawdown
    Historical VaR95
    Historical CVaR95
    Start date
    End date
    Number of observations
This portfolio row is then appended to the summary table.
9. The script builds a correlation matrix to evaluate how strongly the ETFs move together. This helps assess whether diversification is actually effective.
10. The script calculates rolling annualized volatility for each ETF using a 30-day window. This creates a time series that shows how volatility changes through time rather than only reporting one full-sample number.
11. The script creates equity curves for each ETF, tracks each running peak, and calculates drawdowns over time. It also builds the same drawdown series for the equal-weight portfolio and adds it to the drawdown table under PORT_EQW.
12. The script builds rolling historical VaR95 and CVaR95 time series using a 252-day window for every ETF and the equal-weight portfolio.
13. The output is an outputs/ folder (if not already exist), and a risk_metrics.xlsx is saved inside.
14. The exported workbook contains the following sheets:
    Summary
    CorrMatrix
    RollingVol_30D
    Drawdowns
    VaR_95_Roll252
    CVaR_95_Roll252
    Portfolio_Returns
    
The risk_metrics.xlsx is the data for my dashboard and interpretation. For more information on those parts, please see my dashboard and documentation branches.
