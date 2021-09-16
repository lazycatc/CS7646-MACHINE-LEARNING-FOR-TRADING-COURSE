#!/usr/bin/env python
# coding: utf-8



import numpy as np
import pandas as pd
import datetime as dt
import util 




def addIndicators(symbol='IBM',start_date=dt.datetime(2008,1,1),
                  end_date=dt.datetime(2008,2,1),periods=10,plotData=False):
    
    sym=[symbol]
    dates=pd.date_range(start_date,end_date)
    
    
    prices_all = util.get_data(sym,dates)
    prices = prices_all[sym]
    vol_all = util.get_data(sym,dates,colname='Volume')
    vol = vol_all[sym]
    
    
    # add indicators
    ma = prices.rolling(periods).mean()
    std = prices.rolling(periods).std()
    upper_band=ma+(std*2)
    lower_band=ma-(std*2)
    bb = (prices-lower_band)/(std*4)
    psma=prices/ma
    prices_prior=prices.shift(periods-1)
    mm=prices/prices_prior-1
    
    bb=bb.dropna()
    psma=psma.dropna()
    mm=mm.dropna()
    psma=psma.rename(columns={symbol:'price/ma'})
    bb=bb.rename(columns={symbol:'bb'})
    mm=mm.rename(columns={symbol:'mm'})
    
    
    index_bb = pd.qcut(bb['bb'].values, 10, labels= False)
    index_psma = pd.qcut(psma['price/ma'].values, 10, labels= False)

    index_mm = pd.qcut(mm['mm'].values, 10, labels= False)

    states = discretize(index_bb,index_mm, index_psma )
    
    if plotData:
        ma = ma.dropna()
        upper_band=upper_band.dropna()
        lower_band=lower_band.dropna()
        prices_val = prices.loc[prices.index[periods-1:],:]
        ma = ma.rename(columns={symbol: 'sma'})
        upper_band = upper_band.rename(columns={symbol: 'upper_band'})
        lower_band = lower_band.rename(columns={symbol: 'lower_band'})
    
        name1 = upper_band.columns[0]
        name2 = lower_band.columns[0]
        name3 = prices_val.columns[0]
        df_temp = pd.concat([upper_band, lower_band, prices_val], axis=1)
        util.plot_data(df_temp, xlabel= "Date", ylabel="Price")
        

    return states



def discretize(bb, mm, psma):
    return bb + mm * 10 + psma*10*10




if __name__=="__main__":
    addIndicators('IBM', dt.datetime(2008,1,1), dt.datetime(2009,12, 31),10)







