import key
import requests
import json 
import pandas as pd

api_key = key.census_api_key

data_dict = {
    2005: [],
    2007: [],
    2009: [], 
    2012: [],
    2013: [],
    2015: [],
    2017: [],
    2019: [],
    2022: [],
    2023: []
}

label_dict = {
    2005: {

    },
    2007: {

    },
    2009: {

    }, 
    2012: {

    },
    2013: {

    },
    2015: {

    },
    2017: {

    },
    2019: {

    },
    2022: {

    },
    2023: {
        
    }
}

for year in data_dict:
    base_url = "https://api.census.gov/data/" + year + "/acs/acs1/profile?get=NAME"
    geography_code = "&for=congressional district:*"

# 2023 white not latino: DP05_0082PE
# 2023 black not latino: DP05_0083PE
# 2023 native american not latino: DP05_0084PE
# 2023 asian not latino: DP05_0085PE
# 2023 hispanic or latino: DP05_0076PE
url  = "https://api.census.gov/data/2023/acs/acs1/profile?get=NAME,DP05_0082PE,DP05_0083PE,DP05_0084PE,DP05_0085PE,DP05_0076PE&for=congressional district:*&key=" + api_key

data = requests.get(url).json()
#print(data.content)

df = pd.DataFrame(data)
print(df)