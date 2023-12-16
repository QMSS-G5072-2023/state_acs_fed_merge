#Produce the series name for pulling from the FRED Api
import pandas as pd
import os
def unemp_data(states, years):
    from fredapi import Fred
    api_key=os.getenv('FRED_API_KEY')
    fred = Fred(api_key=api_key)

    years_str=  map(str, years) 
    import datetime
    for i in states:
        unemp = 'LAUST' + i + '0000000000003A'
        if states[0]==i:
            data=fred.get_series(unemp)
            pd.unemp=pd.DataFrame(data)
            pd.unemp["STATEFIP"]=i
    
        else:
            data_add=fred.get_series(unemp)
            pd.unemp_add=pd.DataFrame(data_add)
            pd.unemp_add["STATEFIP"]=i
            pd.unemp=pd.unemp._append(pd.unemp_add)
    
    #reset index and subset to years of interest 
    pd.unemp.reset_index(inplace=True) 
    pd.unemp['Year'] = pd.unemp['index'].dt.strftime('%Y').astype(str)
    pd.unemp = pd.unemp[pd.unemp['Year'].isin(years_str)]
    pd.unemp=pd.unemp.rename({0:'Unemployment Rate'}, axis=1)
    pd.unemp=pd.unemp[['STATEFIP','Year', 'Unemployment Rate']]