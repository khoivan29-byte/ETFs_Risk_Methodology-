# Earlier branches of the project focus on pulling ETF market data and calculating risk metrics. This branch focuses on how those results are organized, displayed, and communicated. It includes the completed Excel dashboard workbook and a PDF export of the main dashboard page. 

The dashboard presents the portfolio’s risk profile through these metrics and visual analysis:
  - Annualized Volatility
  - Maximum Drawdown
  - 1-day VaR95
  - 1-day CVaR95
  - Average Correlation to SPY
  - Highest-correlation ETF Pair
  - Portfolio Return Chart
  - Drawdown Chart
  - Correlation Heatmap
  - Maximum Drawdown Episode Section

Inside the workbook, I import data from risk_metrics.xlsx and calculate metrics such as equity (growth of $10,000), peak, drawdown, and returns, on the cumulative scale in the Portfolio_Calc sheet. For the drawdowns, I also use the daily drawdowns to find the Peak to Recovery and Peak to Trough periods in terms of trading days and calendar days. 

The earlier scripts generate raw data and analytics, but this branch turns those results into something easier to interpret and communicate.
