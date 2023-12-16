def ipums_query(states, dir, path, key):    
    #Remove previous extracts from folder 
    import os
    import pandas as pd 
    # Get the current working directory
    cwd = os.getcwd()
    
    #change the directory 
    os.chdir(path)
    
    #remove previoust IPUMS USA extracts 
    import glob, os
    for f in glob.glob("usa_*"):
        os.remove(f)
    
    from pathlib import Path
    from ipumspy import IpumsApiClient, UsaExtract, readers, ddi

    ipums = IpumsApiClient(key)

    import numpy as np
    
    import yaml
    with open("ipums.yml", "r") as stream:
        try:
            print(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)

    #set state id 
    state_id=states
    state_id_int=list(map(int, state_id))

    # Submit an API extract request
    from ipumspy import extract_from_dict
    with open("ipums.yml") as infile:
        extract = extract_from_dict(yaml.safe_load(infile))
        extract.select_cases("STATEFIP", state_id)
    
    ipums.submit_extract(extract)
    print(f"Extract submitted with id {extract.extract_id}")
    
    # wait for the extract to finish
    ipums.wait_for_extract(extract)
    
    # Download the extract
    ipums.download_extract(extract, download_dir=dir)
    



