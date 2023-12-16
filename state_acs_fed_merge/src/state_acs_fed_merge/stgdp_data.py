import pandas as pd
import os
import pickle
import datetime
from fredapi import Fred
api_key=os.getenv('FRED_API_KEY')
fred = Fred(api_key=api_key)

def stgdp_data(states, years): 
    with open('statefip_abv_codes.pkl', 'rb') as fp:
        statefip_dict = pickle.load(fp)
     
    years_str=  map(str, years) 
 
    for i in states:
        for i in states:
            st_abv=statefip_dict.get(i)
            print(st_abv)
            stgdp = st_abv + 'NGSP'
            
            if states[0]==i:
                data=fred.get_series(stgdp)
                pd.stgdp=pd.DataFrame(data)
                pd.stgdp["STATEFIP"]=i
            else:
                data=fred.get_series(stgdp)
                pd.stgdp_add=pd.DataFrame(data)
                pd.stgdp_add["STATEFIP"]=i
                pd.stgdp=pd.stgdp._append(pd.stgdp_add)
    #reset index and subset to years of interest 
    pd.stgdp.reset_index(inplace=True) 
    pd.stgdp['Year'] = pd.stgdp['index'].dt.strftime('%Y').astype(str)
    pd.stgdp = pd.stgdp[pd.stgdp['Year'].isin(years_str)]
    pd.stgdp=pd.stgdp.rename({0:'State GDP'}, axis=1)
    pd.stgdp=pd.stgdp[['STATEFIP','Year', 'State GDP']]