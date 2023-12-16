def acs_summary_stats(states, data,  vars): 
    import pandas as pd
    import os
    import pickle
    
    with open('statefip_codes.pkl', 'rb') as fp:
        statefip_dict = pickle.load(fp)
        #print(statefip_dict)
    
    state_id_int=list(map(int, states))    
    for i in state_id_int:
        if state_id_int[0]==i:
            pd.sum=(data[(data['STATEFIP']==i)].pivot_table(index=[('YEAR')],  values=vars, aggfunc="mean"))
        else:
            pd.sum=pd.sum._append((data[(data['STATEFIP']==i)].pivot_table(index=[('YEAR')],  values=vars, aggfunc="mean")))
    
 