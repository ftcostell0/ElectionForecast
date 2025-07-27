import key
import requests
import json 
import pandas as pd

api_key = key.census_api_key

class ACS:
    data2005 = 'DP01_0017E,DP02_0016E,DP01_0065E,DP01_0066E,DP01_0072E,DP01_0073E,DP01_0074E,DP01_0075E'
    data2007 = 'DP05_0017E,DP02_0066PE,DP05_0066PE,DP05_0072PE,DP05_0073PE,DP05_0074PE,DP05_0075PE'
    data2009 = 'DP05_0017E,DP02_0067PE,DP05_0066PE,DP05_0072PE,DP05_0073PE,DP05_0074PE,DP05_0075PE'
    data2017 = 'DP05_0018E,DP02_0067PE,DP05_0071PE,DP05_0077PE,DP05_0078PE,DP05_0079PE,DP05_0080PE'
    data2019 = 'DP05_0018E,DP02_0068PE,DP05_0071PE,DP05_0077PE,DP05_0078PE,DP05_0079PE,DP05_0080PE'
    data2022 = 'DP05_0018E,DP02_0068PE,DP05_0073PE,DP05_0079PE,DP05_0080PE,DP05_0081PE,DP05_0082PE'
    data2023 = 'DP05_0018E,DP02_0068PE,DP05_0076PE,DP05_0082PE,DP05_0083PE,DP05_0084PE,DP05_0085PE'

    dict2005 = {
        'DP01_0017E':'median_age','DP02_0016E':'bachelors_degree','DP01_0065E':'total_pop',
        'DP01_0066E':'latino','DP01_0072E':'white','DP01_0073E':'black','DP01_0074E':'native','DP01_0075E':'asian'
    }

    dict2007 = {
        'DP05_0017E':'median_age','DP02_0066PE':'bachelors_degree','DP05_0066PE':'latino',
        'DP05_0072PE':'white','DP05_0073PE':'black','DP05_0074PE':'native','DP05_0075PE':'asian'
    }

    dict2009 = {
        'DP05_0017E':'median_age','DP02_0067PE':'bachelors_degree','DP05_0066PE':'latino',
        'DP05_0072PE':'white','DP05_0073PE':'black','DP05_0074PE':'native','DP05_0075PE':'asian'
    }

    dict2017 = {
        'DP05_0018E':'median_age','DP02_0067PE': 'bachelors_degree','DP05_0071PE':'latino',
        'DP05_0077PE':'white','DP05_0078PE':'black','DP05_0079PE':'native','DP05_0080PE':'asian'
    }

    dict2019 = {
        'DP05_0018E':'median_age','DP02_0068PE':'bachelors_degree','DP05_0071PE':'latino',
        'DP05_0077PE':'white','DP05_0078PE':'black','DP05_0079PE':'native','DP05_0080PE':'asian'
    }
    dict2022 = {
        'DP05_0018E':'median_age','DP02_0068PE':'bachelors_degree','DP05_0073PE':'latino',
        'DP05_0079PE':'white','DP05_0080PE':'black','DP05_0081PE':'native','DP05_0082PE':'asian'
    }

    dict2023 = {
        'DP05_0018E':'median_age','DP02_0068PE':'bachelors_degree','DP05_0076PE':'latino',
        'DP05_0082PE':'white','DP05_0083PE':'black','DP05_0084PE':'native','DP05_0085PE':'asian'
    }

    classDict = {
        2005: [data2005, dict2005],
        2007: [data2007, dict2007],
        2009: [data2009, dict2009],
        2012: [data2009, dict2009],
        2013: [data2009, dict2009],
        2015: [data2009, dict2009],
        2017: [data2017, dict2017],
        2019: [data2019, dict2019],
        2022: [data2022, dict2022],
        2023: [data2023, dict2023]
    }

    def __init__(self,year):
        self.data = self.classDict[year][0]
        self.labels = self.classDict[year][1]

years = [2005, 2007, 2009, 2012, 2013, 2015, 2017, 2019, 2022, 2023]

for year in years:
    survey = ACS(year)
    url = "https://api.census.gov/data/" + str(year) + "/acs/acs1/profile?get=NAME," + survey.data + "&for=congressional district:*&key=" + api_key
    response = requests.get(url)
    data = response.json()

    df = pd.DataFrame(data[1:], columns=data[0])  # Create DataFrame and drop the first row
    df.drop(index=0, inplace=True)  
    df = df.rename(columns=survey.labels)

    print(df)

# 2023 white not latino: DP05_0082PE
# 2023 black not latino: DP05_0083PE
# 2023 native american not latino: DP05_0084PE
# 2023 asian not latino: DP05_0085PE
# 2023 hispanic or latino: DP05_0076PE
#url  = "https://api.census.gov/data/2023/acs/acs1/profile?get=NAME,DP05_0082PE,DP05_0083PE,DP05_0084PE,DP05_0085PE,DP05_0076PE&for=congressional district:*&key=" + api_key
