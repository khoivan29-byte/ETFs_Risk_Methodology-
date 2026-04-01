#The file in this branch, risk_metrics.py, is responsible for transforming market return data into portfolio-level analytics. It builds the equal-weight ETF portfolio, computes performance and downside-risk measures, and generates the metric outputs used in the final Excel dashboard.
The script performs the main portfolio analytics tasks:

1. The script imports the cleaned ETF return dataset (a CSV file in this case). It loads the data into a pandas DataFrame, with dates as the time index and ETF tickers as columns.
2. Before running analytics, the script checks if the input data is in the expected format. This may include: confirming that required ETF columns are present, handling missing values, aligning date indices, and ensuring numeric return values are stored correctly.
3. Starting from an initial portfolio value, the script compounds returns over time to create the portfolio’s equity curve.
4. Then, it tracks how much the portfolio gained or lost relative to its starting value.
5. From the gains and losses, the script calculates how far the portfolio falls below its prior peak and identifies the worst peak-to-trough decline in the sample.
6. The script estimates how much the portfolio typically fluctuates on a year-scaled basis.
7. The script estimates the portfolio’s downside tail risk using historical daily returns:
    VaR gives a “bad day” loss threshold
    CVaR shows the average loss during the worst days
8. The script builds a correlation matrix to evaluate how strongly the ETFs move together. This helps assess whether diversification is actually effective.

For more information on the methodology and reasoning, please see my docx memo
