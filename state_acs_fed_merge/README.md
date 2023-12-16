# state_acs_fed_merge

Package ffor merging annual state-level American Community Survey data with state-level data from the federal reserve.

## Installation

```bash
$ pip install state_acs_fed_merge
```

## Usage

-   Pull annual state-level data from American Community Survey and merge with state-level minumum wage, 
    unemployment, and gdp data for those states and years.

    This function determines the average of any requested variable available in the American
    Community Survey data for a specific state and year using data queried from IPUMS-ACS :
    https://usa.ipums.org/usa/

    It then draws data from the Federal Reserve on annual state-level data that is readily available, 
    including  tate-level minumum wage, unemployment, and gdp data for those states and years.  
    Federal reserve data is pulled from https://fred.stlouisfed.org/. 
    
    The input are: 
    state_list : str
        list of state fip codes for states that you would like to pull data on 
        see state fip codes here:https://transition.fcc.gov/oet/info/maps/census/fips/fips.txt
        
    years : int
        single year or list of years for which you would like data 

    var_list : str
        list of variables from the American Community Survey for which you would like state-leve avarages. 
        see variable list here: https://usa.ipums.org/usa-action/variables/search 

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`state_acs_fed_merge` was created by Sophie Collyer. It is licensed under the terms of the MIT license.

## Credits

`state_acs_fed_merge` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
