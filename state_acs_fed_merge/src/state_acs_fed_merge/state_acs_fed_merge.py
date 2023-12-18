# install necessary packages 
import pip
import sys, subprocess; subprocess.run([sys.executable, '-m', 'pip', 'install', 'ipumspy'])

# import relevant packages 
import os
import pickle
import numpy as np
import pandas as pd
from ipumspy import IpumsApiClient, UsaExtract, readers, ddi
from pathlib import Path
from decouple import config
from dotenv import load_dotenv
load_dotenv()
IPUMS_API_KEY = os.getenv('IPUMS_API_KEY')
FRED_API_KEY = os.getenv('FRED_API_KEY')


def state_acs_fed_merge(state_list =["55", "56"] , years=[2018, 2019], var_list = ["STATEFIP", "POVERTY", "INCEARN", "RENT", "INCWAGE"]):
    """
    Pull annual state-level data from American Community Survey and merge with state-level minumum wage, 
    unemployment, and gdp data for those states and years.

    This function determines the average of any requested variable available in the American
    Community Survey data for a specific state and year using data queried from IPUMS-ACS :
    https://usa.ipums.org/usa/

    It then draws data from the Federal Reserve on annual state-level data that is readily available, 
    including  tate-level minumum wage, unemployment, and gdp data for those states and years.  
    Federal reserve data is pulled from https://fred.stlouisfed.org/. 
    
    Parameters
    ----------
    state_list : str
        list of state fip codes for states that you would like to pull data on 
        see state fip codes here:https://transition.fcc.gov/oet/info/maps/census/fips/fips.txt
        
    years : int
        single year or list of years for which you would like data 

    var_list : str
        list of variables from the American Community Survey for which you would like state-leve avarages. 
        see variable list here: https://usa.ipums.org/usa-action/variables/search
    
    Returns
    -------
    csv file organized by state and year showing the average for the input variables from the ACS and state-level minumum wage, 
    unemployment, and gdp data for those states and years.

    Examples
    --------
    acs_fed_state_match(state_list =["55", "56"] , years=[2018, 2019], var_list = ["STATEFIP", "POVERTY",  "INCEARN", "RENT", "INCWAGE"])

    produces csv and pandas tables with average rates of poverty, earnings, rent, and wages in Wisconsin and Wyoming for 2018 and 2019.

    """
    # prepare for impums extract 
    IPUMS_API_KEY = config('IPUMS_API_KEY')
    path = os.getcwd()  
    download_dir = Path(path)

    # build the yml to upload to IPUMS API
    import ipums_yml
    ipums_yml.ipums_yml(years, var_list)

    # query the IPUMS API
    import ipums_api_query
    ipums_api_query.ipums_query(state_list, download_dir, path, IPUMS_API_KEY)
    
    # import the data into python
    ddi_file = list(download_dir.glob("*.xml"))[0]
    ddi = readers.read_ipums_ddi(ddi_file)
    pd.ipums_df = readers.read_microdata(ddi, download_dir / ddi.file_description.filename)
    pd.ipums_df.head()
    pd.ipums_df_fa=pd.ipums_df[((pd.ipums_df['GQ']==1)|(pd.ipums_df['GQ']==3)|(pd.ipums_df['GQ']==5))]
    
    # clean the data
    import acs_data_clean
    if 'POVERTY' in var_list:
        pd.ipums_df_fa=acs_data_clean.poverty(pd.ipums_df_fa)
    if 'INCWAGE' in var_list:
        pd.ipums_df_fa=acs_data_clean.incwage(pd.ipums_df_fa)
    if 'RENT' in var_list:
        pd.ipums_df_fa=acs_data_clean.rent(pd.ipums_df_fa)
    if 'RENTGRS' in var_list:
        pd.ipums_df_fa=acs_data_clean.rentgrs(pd.ipums_df_fa)
    
    # produce summary statistics 
    import acs_summary_stats
    acs_summary_stats.acs_summary_stats(state_list,pd.ipums_df_fa, var_list)
    pd.state_yr_acs=pd.sum

    # pull state-level data from FRED 
    import unemp_data
    import minwage_data
    import stgdp_data
    unemp_data.unemp_data(state_list, years)
    minwage_data.minwage_data(state_list, years)
    stgdp_data.stgdp_data(state_list, years)
    pd.fred_data=pd.merge(pd.stgdp, pd.mw, on=(['STATEFIP', 'Year']), how='inner')
    pd.fred_data=pd.merge(pd.fred_data, pd.unemp, on=(['STATEFIP', 'Year']), how='inner')

    # merge fred and IPUMS data
    pd.state_yr_acs.reset_index(inplace=True) 
    pd.state_yr_acs=pd.state_yr_acs.rename({'YEAR':'Year'}, axis=1).astype(object)
    pd.state_yr_acs["STATEFIP"]=pd.state_yr_acs["STATEFIP"].apply(pd.to_numeric) 
    pd.state_yr_acs['STATEFIP'] = pd.state_yr_acs['STATEFIP'].apply(lambda x: round(x))
    pd.state_yr_acs['Year'] = pd.state_yr_acs['Year'].apply(pd.to_numeric) 
    pd.fred_data['STATEFIP'] = pd.fred_data['STATEFIP'].apply(pd.to_numeric) 
    pd.fred_data['Year'] = pd.fred_data['Year'].apply(pd.to_numeric) 
    pd.final_data=pd.merge(pd.fred_data, pd.state_yr_acs, on=(['STATEFIP', 'Year']), how='outer')
    pd.final_data['STATEFIP'] = pd.fred_data['STATEFIP'].astype(str)

    # add state names to table
    with open('statefip_abv_codes.pkl', 'rb') as fp:
        statefip_dict = pickle.load(fp)
    pd.final_data['State Name'] = ""
    
    for i in state_list:
        st_abv=statefip_dict.get(i)
        print(st_abv)
        pd.final_data['State Name'] = np.where(pd.final_data['STATEFIP']==i, st_abv,  pd.final_data['State Name'])

    # order columns for export
    cols = list(pd.final_data)
    cols = [cols[-1]] + cols[:-1]
    pd.final_data = pd.final_data[cols]

    # export CSV
    pd.final_data.to_csv(r"\ipums_fred_merge_extract.csv", index=False)

    return(pd.final_data.head())
    
      