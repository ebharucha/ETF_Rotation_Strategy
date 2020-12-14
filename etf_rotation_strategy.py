#########################################################################
# Drawing Inspiration from the ETF Rotation System by The Lazy Trader
# http://www.the-lazy-trader.com/2015/01/ETF-Rotation-Systems-to-beat-the-Market-SPY-IWM-EEM-EFA-TLT-TLH-DBC-GLD-ICF-RWX.html
# Identify the top "n" ETFs based on particular weightings applied to
# (1) The 3 months return 
# (2) The 20 day return
# (3) The 20 days volatility 
# List of ETFs defined in "etfs" in the main function
# ebharucha: 12/12/2020
########################################################################

# Import dependencies
import numpy as np
import pandas as pd
import yfinance as yf
import time
import warnings
warnings.filterwarnings("ignore")

# Class to compute ETF metrics described at the top of this file
class etfMetrics():
    def __init__(self, sym):
        self.sym = sym
        etf = yf.Ticker(sym)
        self.etf_data = etf.history(period="90d")
        self.etf_data['OneDayReturn'] = self.etf_data.Close.pct_change()
        
    def Return90d(self):
        return (self.etf_data.Close[-1] - self.etf_data.Close[-90])/self.etf_data.Close[-90]
    
    def Return20d(self):
        return (self.etf_data.Close[-1] - self.etf_data.Close[-20])/self.etf_data.Close[-20]
    
    def Vol20d(self):
        return (self.etf_data.OneDayReturn[-20:].std()*np.sqrt(252))
      
def create_ranked_metrics(etf_metrics):
    # Store metrics in DataFrame
    symbols = []
    return90d = []
    return20d = []
    vol20d = []
    for (k,v) in etf_metrics.items():
        symbols.append(k)
        return90d.append(v.Return90d())
        return20d.append(v.Return20d())
        vol20d.append(v.Vol20d())
    df_etf = pd.DataFrame()
    df_etf['Symbols'] = symbols
    df_etf['Return90d'] = return90d
    df_etf['Return20d'] = return20d
    df_etf['Vol20d'] = vol20d
    
    # Rank metrics
    df_etf['Return90d_rank'] = df_etf.Return90d.rank(ascending=False)
    df_etf['Return20d_rank'] = df_etf.Return20d.rank(ascending=False)
    df_etf['Vol20d_rank'] = df_etf.Vol20d.rank(ascending=True)

    # Weighted ranking
    weights = [0.4, 0.3, 0.3]
    weighted_ranks = []
    for idx, row in df_etf.iterrows():
        weighted_ranks.append(row.Return90d_rank*weights[0] + row.Return20d_rank*weights[1] + row.Vol20d_rank*weights[2])   
    df_etf['Weighted_rank'] = weighted_ranks
    df_etf['Overall_rank'] = df_etf.Weighted_rank.rank(ascending=True)
    df_etf = df_etf.sort_values(by='Overall_rank').reset_index(drop=True)

    return(df_etf)

# List of ETFs to evaluate
etfs = ['SPY', 'QQQ', 'IWM', 'EEM', 'EFA', 'TLT', 'TLH', 'DBC', 'GLD', 'ICF', 'RWX']
n = 3
# Capture  metrics for each ETF & store in dictionary 
etf_metrics = {etf: etfMetrics(etf) for etf in etfs}
df_etf = create_ranked_metrics(etf_metrics)

f = lambda x:f'{x*100:.2f}%'
df_etf['Return90d'] = df_etf['Return90d'].apply(f)
df_etf['Return20d'] = df_etf['Return20d'].apply(f)
df_etf['Vol20d'] = df_etf['Vol20d'].apply(f)

if __name__ == "__main__":
    # Print top "n"  ranked ETFs
    print(f'Top "{n}" ETFs : {df_etf.head(n).Symbols.values}\n')
    # Print & write DataFrame of computed metrics to CSV
    print(df_etf)
    date = time.strftime("%Y%m%d")
    df_etf.to_csv(f'./ranked_etfs_{date}.csv')
