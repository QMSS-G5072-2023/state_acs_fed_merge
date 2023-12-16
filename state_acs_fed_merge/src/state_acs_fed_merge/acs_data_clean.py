import pandas as pd
import os
import numpy as np

def poverty(data): 
    data=data.rename(columns={"POVERTY" : "INCNEEDS"})
    data['POVERTY'] = np.where(data['INCNEEDS']<100 , 1, 0)
    return data   
    
def incwage(data):
    data['INCWAGE'] = np.where(data['INCWAGE']>=999998 , 0, data['INCWAGE']).astype(float)
    return data   
    
def rent(data): 
    data['RENT2'] = np.where(data['RENT']==0 , np.nan, data['RENT']).astype(float)
    #TEST
    rent_wna = data['RENT2'].mean() #data = data
    rent_ss=data[(data['RENT']!=0)]['RENT'].mean() 
    print(rent_wna, rent_ss)
    return data

def rentgrs(data): 
    data['RENTGRS2'] = np.where(data['RENTGRS']==0 , np.nan, data['RENTGRS']).astype(float)
    rent_grs_wna = data['RENTGRS2'].mean() #data = data
    rentgrs_ss=data[(data['RENT']!=0)]['RENT'].mean() 
    print(rent_grs_wna, rentgrs_ss )
    return data       