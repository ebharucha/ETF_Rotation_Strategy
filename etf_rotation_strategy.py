#########################################################################
# Drawing Inspiration from the ETF Rotation System by The Lazy Trader
# http://www.the-lazy-trader.com/2015/01/ETF-Rotation-Systems-to-beat-the-Market-SPY-IWM-EEM-EFA-TLT-TLH-DBC-GLD-ICF-RWX.html
# Identify the top "n" ETFs based on particular weightings applied to
# (1) The 3 months return 
# (2) The 20 day return
# (3) The 20 days volatility 
# List of ETFs defined in "etfs" in the main function
# ebharucha: 12/28/2020
########################################################################

# Import dependencies
import sys
import os.path
import numpy as np
import pandas as pd
import pandas_datareader as web
import datetime
from dateutil.relativedelta import relativedelta
import warnings
warnings.filterwarnings("ignore")

# Class to compute ETF metrics described at the top of this file
class etfMetrics():
    def __init__(self, sym, start_date, end_date):
        self.sym = sym
        self.error = ''
        try:
            self.etf_data = web.get_data_yahoo(sym,
                                start = start_date,
                                end=end_date)
        except:
            print(f'Could not retireve data for "{sym}"')
            self.error = f'Could not retireve data for "{sym}"'
            return (self.error)
        self.etf_data['OneDayReturn'] = self.etf_data['Adj Close'].pct_change()
        
    def Return3M(self):
        return (self.etf_data['Adj Close'].resample('3M').ffill().pct_change()[1])
    
    def Return20D(self):
        return (self.etf_data['Adj Close'][-1] - self.etf_data['Adj Close'][-21])/self.etf_data['Adj Close'][-21]
    
    def Vol20D(self):
        return (self.etf_data.OneDayReturn[-21:].std()*np.sqrt(252))
      
def create_ranked_metrics(etf_metrics):
    # Store metrics in DataFrame
    symbols = []
    return3M = []
    return20D = []
    vol20D = []
    for (k,v) in etf_metrics.items():
        symbols.append(k)
        return3M.append(v.Return3M())
        return20D.append(v.Return20D())
        vol20D.append(v.Vol20D())
    df_etf = pd.DataFrame()
    df_etf['Symbols'] = symbols
    df_etf['Return3M'] = return3M
    df_etf['Return20D'] = return20D
    df_etf['Vol20D'] = vol20D
    
    # Rank metrics
    df_etf['Return3M_rank'] = df_etf.Return3M.rank(ascending=False)
    df_etf['Return20D_rank'] = df_etf.Return20D.rank(ascending=False)
    df_etf['Vol20D_rank'] = df_etf.Vol20D.rank(ascending=True)

    # Weighted ranking
    weights = [0.4, 0.3, 0.3]
    weighted_ranks = []
    for idx, row in df_etf.iterrows():
        weighted_ranks.append(f'{row.Return3M_rank*weights[0] + row.Return20D_rank*weights[1] + row.Vol20D_rank*weights[2]:.1f}')   
    df_etf['Weighted_rank'] = weighted_ranks
    df_etf['Overall_rank'] = df_etf.Weighted_rank.rank(ascending=True)
    df_etf = df_etf.sort_values(by='Overall_rank').reset_index(drop=True)

    return(df_etf)

# Start of main program
# List of ETFs to evaluate
file = 'etfs.txt'
if (len(sys.argv) > 1):
    etfs = sys.argv[1:]
elif os.path.isfile(f'{file}'):
    try:
        with open(f'{file}', 'r') as f:
            etfs = f.readlines()
    except:
        print (f'Could not open "{file}"')
    etfs = etfs[0].split()
    os.remove(f'{file}')
else:
    etfs = ['SPY', 'QQQ', 'IWM', 'EEM', 'EFA', 'TLT', 'TLH', 'DBC', 'GLD', 'ICF', 'RWX']
n = 3  # Specify number of top ETFs to rank
today = str(datetime.date.today())
date_3mago = str(datetime.date.today() + relativedelta(months=-4))

# Capture  metrics for each ETF & store in dictionary 
etf_metrics = {etf: etfMetrics(etf, date_3mago, today) for etf in etfs}
df_etf = create_ranked_metrics(etf_metrics)

f = lambda x:f'{x*100:.2f}%'
df_etf['Return3M'] = df_etf['Return3M'].apply(f)
df_etf['Return20D'] = df_etf['Return20D'].apply(f)
df_etf['Vol20D'] = df_etf['Vol20D'].apply(f)

if __name__ == "__main__":
    # Print top "n"  ranked ETFs
    print (f'Date: {today}')
    print(f'Top "{n}" ETFs : {df_etf.head(n).Symbols.values}\n')
    # Print & write DataFrame of computed metrics to CSV
    print(df_etf.to_string(index=False))
    df_etf.to_csv(f'./ranked_etfs_{today}.csv')


