#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime as dt
import os
import numpy as np
import pandas as pd
from util import get_data, plot_data


# In[2]:


def author():
    return 'name_id'


# In[3]:


def compute_portvals(
    order_file,
    start_val=1000000,
    commission=9.95,
    impact=0.005
):
    
    
    
    # order csv file
    order = order_file
    order =order.sort_index()

    
    
    # dates 
    start_date = order.index[0]
    end_date = order.index[-1]
    dates = pd.date_range(start_date, end_date, freq='D')
    df = pd.DataFrame(index=dates)
    
    
    # symbols
    symbols = []
    for index, row in order.iterrows():
        if row['Symbol'] not in symbols:
            symbols.append(row['Symbol'])
            
    

    
    prices = df.copy()
    for symbol in symbols:
        df_temp = pd.read_csv('../data/{}.csv'.format(symbol),parse_dates=True,
                              index_col='Date',usecols=['Date','Adj Close'],na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close':symbol})
        prices = prices.join(df_temp,how='inner')
        
    prices['cash']=np.ones((prices.shape[0],1))
    
        
                           
                           
    trades=prices.copy()
    trades[:]=0
    for index, row in order.iterrows():
                        if row['Order']=='BUY':
                           trades.at[index,row['Symbol']] += row['Shares']
                           cost = commission + prices.at[index, row['Symbol']]*row['Shares']*(1+impact)
                           trades.at[index,'cash'] -= cost
                        else:
                            trades.at[index,row['Symbol']] -= row['Shares']
                            cost = prices.at[index, row['Symbol']]*row['Shares']*(1-impact)-commission
                            trades.at[index,'cash'] += cost
                           
                           
    holdings = trades.copy()
    holdings.at[start_date,'cash']=holdings.at[start_date,'cash']+start_val
    holdings=holdings.cumsum(axis=0)
    
                           
    values=prices*holdings
    values['Sum']=values.sum(axis=1)
    portvals = values.drop(values.columns[:-1], axis=1)

                        
                    
    return portvals  


# In[4]:


def test_code(): 
    
    of = '../orders-02.csv'
    sv = 1000000 
    

    
    # Process orders  
    portvals = compute_portvals(order_file=of, start_val=sv)  
    
    
    if isinstance(portvals, pd.DataFrame):  
        portvals = portvals[portvals.columns[0]]  # just get the first column  		  	   		   	 			  		 			 	 	 		 		 	
    else:  
        "warning, code did not return a DataFrame" 
        
 

        
    # Get portfolio stats 
    # Here we just fake the data. you should use your code from previous assignments. 
    start_date = dt.datetime(2008, 1, 1) 
    end_date = dt.datetime(2008, 6, 1) 
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]  
                                                           
        
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]  
    
      
    
    # Compare portfolio against $SPX  
    print('Date Range: {} to {}'.format(start_date, end_date)) 
    print()  
    print('Sharpe Ratio of Fund: {}'.format(sharpe_ratio)) 
    print('Sharpe Ratio of SPY : {}'.format(sharpe_ratio_SPY))  
    print() 
    print('Cumulative Return of Fund: {}'.format(cum_ret))  
    print('Cumulative Return of SPY : {}'.format(cum_ret_SPY)) 
    print()  
    print('Standard Deviation of Fund: {}'.format(std_daily_ret))  
    print('Standard Deviation of SPY : {}'.format(std_daily_ret_SPY)) 
    print()  
    print('Average Daily Return of Fund: {}'.format(avg_daily_ret))
    print('Average Daily Return of SPY : {}'.format(avg_daily_ret_SPY))
    print() 
    print('Final Portfolio Value: {}'.format(portvals[-1])) 


# In[24]:


if __name__ == '__main__':  
    test_code() 


# In[ ]:




