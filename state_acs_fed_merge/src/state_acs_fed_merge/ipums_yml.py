# imports 
import os
import yaml
from ruamel.yaml.main import round_trip_dump as yaml_dump
from ruamel.yaml.comments import \
        CommentedMap as OrderedDict, \
        CommentedSeq as OrderedList

# get the current working directory and change the directory 
cwd = os.getcwd()
os.chdir('/Users/Sophie/Documents/GitHub/Collyer_Sophie/Final_Project')

# prepare the yml file
def ipums_yml(years=[2021, 2020], vars=["AGE" ,"SEX", "STATEFIP", "POVERTY", "RENT", "RENTGRS"]):
    """Prepare the yml file for IPUMS API query"""
    # prepare year inputs for producing yml file
    years_str = map(str, years) 
    years_yml = ["us"+y+ "a" for y in years_str]
        
    # prepare and save yml file to upload to IPUMS API 
    ipums_yml = OrderedDict({
        "collection": "usa",
        "samples": OrderedList(years_yml),
        "variables": OrderedList(vars)})
        
    # dump the yaml file
    with open('ipums.yml', 'w') as file:
        yaml_dump(ipums_yml, file)
    print(open('ipums.yml').read())
