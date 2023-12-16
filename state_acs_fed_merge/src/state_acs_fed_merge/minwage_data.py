import pandas as pd
import os
import pickle
import datetime
from fredapi import Fred
api_key=os.getenv('FRED_API_KEY')
fred = Fred(api_key=api_key)

def minwage_data(states, years): 
    with open('statefip_abv_codes.pkl', 'rb') as fp:
        statefip_dict = pickle.load(fp)
     
    years_str=  map(str, years) 
 
    for i in states:
        for i in states:
            st_abv=statefip_dict.get(i)
            print(st_abv)
            minwage = 'STTMINWG' + st_abv  
            
            if states[0]==i:
                data=fred.get_series(minwage)
                pd.mw=pd.DataFrame(data)
                pd.mw["STATEFIP"]=i
            else:
                data=fred.get_series(minwage)
                pd.mw_add=pd.DataFrame(data)
                pd.mw_add["STATEFIP"]=i
                pd.mw=pd.mw._append(pd.mw_add)
    #reset index and subset to years of interest 
    pd.mw.reset_index(inplace=True) 
    pd.mw['Year'] = pd.mw['index'].dt.strftime('%Y').astype(str)
    pd.mw = pd.mw[pd.mw['Year'].isin(years_str)]
    pd.mw=pd.mw.rename({0:'Minimum Wage'}, axis=1)
    pd.mw=pd.mw[['STATEFIP','Year', 'Minimum Wage']]