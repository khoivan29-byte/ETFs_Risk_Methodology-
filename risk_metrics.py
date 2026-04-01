import os
import numpy as np
import pandas as pd

CONF_LEVEL = 0.95 #Confidence level for VaR/CVaR
ROLLING_WINDOW = 30 #For rolling volatility (in days)
TRADING_DAYS = 252 #Typical number of trading days in a year

#Load data from Step 1
prices = pd.read_csv("data/prices.csv", index_col=0, parse_dates=True) 
returns = pd.read_csv("data/returns.csv", index_col=0, parse_dates=True)

#Align dates
common_index = prices.index.intersection(returns.index)
prices = prices.loc[common_index].sort_index()
returns = returns.loc[common_index].sort_index()

tickers = list(returns.columns)

#Risk metrics functions
def max_drawdown_from_returns(r: pd.Series) -> float:
    """Max drawdown from return series (as a negative number)."""
    equity = (1 + r.fillna(0)).cumprod() 
    peak = equity.cummax()
    dd = equity / peak - 1
    return dd.min()

def hist_var_cvar(r: pd.Series, conf: float = 0.95):
    """Historical VaR/CVaR at confidence level conf. Returns positive numbers (loss magnitudes)."""
    x = r.dropna().values
    if len(x) < 10:
        return np.nan, np.nan
    q = np.quantile(x, 1 - conf)          #Left tail return (negative usually)
    var = -q                               #Convert to positive loss
    tail = x[x <= q]
    cvar = -tail.mean() if len(tail) > 0 else np.nan
    return var, cvar

#Per-ETF summary metrics
summary_rows = []
for t in tickers:
    r = returns[t]
    vol_ann = r.std() * np.sqrt(TRADING_DAYS)
    mdd = max_drawdown_from_returns(r)
    var, cvar = hist_var_cvar(r, CONF_LEVEL)
    corr_spy = r.corr(returns["SPY"]) if "SPY" in returns.columns and t != "SPY" else (1.0 if t == "SPY" else np.nan)

    summary_rows.append({
        "Ticker": t,
        "Ann_Vol": vol_ann,
        "Max_Drawdown": mdd,
        f"VaR_{int(CONF_LEVEL*100)}": var,
        f"CVaR_{int(CONF_LEVEL*100)}": cvar,
        "Corr_with_SPY": corr_spy,
        "Start_Date": r.dropna().index.min(),
        "End_Date": r.dropna().index.max(),
        "Num_Obs": int(r.dropna().shape[0])
    })

summary = pd.DataFrame(summary_rows).set_index("Ticker").sort_index()

#Portfolio (equal-weight) metrics
w = np.repeat(1/len(tickers), len(tickers))
port_ret = returns[tickers].fillna(0).dot(w)
port_ret_df = pd.DataFrame({"PORT_EQW": port_ret})
port_vol_ann = port_ret.std() * np.sqrt(TRADING_DAYS)
port_mdd = max_drawdown_from_returns(port_ret)
port_var, port_cvar = hist_var_cvar(port_ret, CONF_LEVEL)

portfolio_row = pd.DataFrame([{
    "Ann_Vol": port_vol_ann,
    "Max_Drawdown": port_mdd,
    f"VaR_{int(CONF_LEVEL*100)}": port_var,
    f"CVaR_{int(CONF_LEVEL*100)}": port_cvar,
    "Corr_with_SPY": np.nan,
    "Start_Date": port_ret.dropna().index.min(),
    "End_Date": port_ret.dropna().index.max(),
    "Num_Obs": int(port_ret.dropna().shape[0])
}], index=["PORT_EQW"])

summary_with_port = pd.concat([summary, portfolio_row], axis=0)

#Corr matrix
corr = returns[tickers].corr()

#Rolling 30D volatility (annualized)
rolling_vol = returns[tickers].rolling(ROLLING_WINDOW).std() * np.sqrt(TRADING_DAYS)

#Drawdowns  
equity_curves = (1 + returns[tickers].fillna(0)).cumprod()
peaks = equity_curves.cummax()
drawdowns = equity_curves / peaks - 1

#Portfolio drawdown
port_equity = (1 + port_ret.fillna(0)).cumprod()
port_peak = port_equity.cummax()
port_dd = port_equity / port_peak - 1
drawdowns["PORT_EQW"] = port_dd

#VaR/CVaR time series 
#Rolling historical VaR/CVaR using a 252-day window
ROLL_VAR_WINDOW = 252

def rolling_hist_var(series: pd.Series, conf=0.95, window=252):
    out = series.rolling(window).apply(lambda x: -np.quantile(x, 1-conf), raw=False)
    return out

def rolling_hist_cvar(series: pd.Series, conf=0.95, window=252):
    def cvar_func(x):
        q = np.quantile(x, 1-conf)
        tail = x[x <= q]
        return -tail.mean() if len(tail) > 0 else np.nan
    return series.rolling(window).apply(lambda x: cvar_func(np.array(x)), raw=False)

var_ts = pd.DataFrame(index=returns.index)
cvar_ts = pd.DataFrame(index=returns.index)

for t in tickers:
    var_ts[t] = rolling_hist_var(returns[t].dropna(), CONF_LEVEL, ROLL_VAR_WINDOW)
    cvar_ts[t] = rolling_hist_cvar(returns[t].dropna(), CONF_LEVEL, ROLL_VAR_WINDOW)

#Portfolio rolling VaR/CVaR
var_ts["PORT_EQW"] = rolling_hist_var(port_ret, CONF_LEVEL, ROLL_VAR_WINDOW)
cvar_ts["PORT_EQW"] = rolling_hist_cvar(port_ret, CONF_LEVEL, ROLL_VAR_WINDOW)

#Export to Excel
os.makedirs("outputs", exist_ok=True)
out_path = "outputs/risk_metrics.xlsx"

with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
    summary_with_port.to_excel(writer, sheet_name="Summary")
    corr.to_excel(writer, sheet_name="CorrMatrix")
    rolling_vol.to_excel(writer, sheet_name="RollingVol_30D")
    drawdowns.to_excel(writer, sheet_name="Drawdowns")
    var_ts.to_excel(writer, sheet_name=f"VaR_{int(CONF_LEVEL*100)}_Roll252")
    cvar_ts.to_excel(writer, sheet_name=f"CVaR_{int(CONF_LEVEL*100)}_Roll252")
    port_ret_df.to_excel(writer, sheet_name="Portfolio_Returns")

print("Step 2 complete.")
print(f"Saved: {out_path}")
print("Sheets:", ["Summary","CorrMatrix","RollingVol_30D","Drawdowns",
                 f"VaR_{int(CONF_LEVEL*100)}_Roll252", f"CVaR_{int(CONF_LEVEL*100)}_Roll252"])
