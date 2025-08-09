import key
import requests
import json 
import pandas as pd

api_key = key.census_api_key

class ACS:
    data2005 = 'DP01_0017E,DP02_0016E,DP01_0065E,DP01_0066E,DP01_0072E,DP01_0073E,DP01_0074E,DP01_0075E'
    data2007 = 'DP05_0017E,DP02_0066E,DP05_0066PE,DP05_0072PE,DP05_0073PE,DP05_0074PE,DP05_0075PE'
    data2009 = 'DP05_0017E,DP02_0067E,DP05_0066PE,DP05_0072PE,DP05_0073PE,DP05_0074PE,DP05_0075PE'
    data2012 = 'DP05_0017E,DP02_0067PE,DP05_0066PE,DP05_0072PE,DP05_0073PE,DP05_0074PE,DP05_0075PE'
    data2017 = 'DP05_0018E,DP02_0067PE,DP05_0071PE,DP05_0077PE,DP05_0078PE,DP05_0079PE,DP05_0080PE'
    data2019 = 'DP05_0018E,DP02_0068PE,DP05_0071PE,DP05_0077PE,DP05_0078PE,DP05_0079PE,DP05_0080PE'
    data2022 = 'DP05_0018E,DP02_0068PE,DP05_0073PE,DP05_0079PE,DP05_0080PE,DP05_0081PE,DP05_0082PE'
    data2023 = 'DP05_0018E,DP02_0068PE,DP05_0076PE,DP05_0082PE,DP05_0083PE,DP05_0084PE,DP05_0085PE'

    dict2005 = {
        'DP01_0017E':'median_age','DP02_0016E':'bachelors_degree','DP01_0065E':'total_pop',
        'DP01_0066E':'latino','DP01_0072E':'white','DP01_0073E':'black','DP01_0074E':'native','DP01_0075E':'asian'
    }

    dict2007 = {
        'DP05_0017E':'median_age','DP02_0066E':'bachelors_degree','DP05_0066PE':'latino',
        'DP05_0072PE':'white','DP05_0073PE':'black','DP05_0074PE':'native','DP05_0075PE':'asian'
    }

    dict2009 = {
        'DP05_0017E':'median_age','DP02_0067E':'bachelors_degree','DP05_0066PE':'latino',
        'DP05_0072PE':'white','DP05_0073PE':'black','DP05_0074PE':'native','DP05_0075PE':'asian'
    }

    dict2012 = {
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
        2012: [data2012, dict2012],
        2013: [data2012, dict2012],
        2015: [data2012, dict2012],
        2017: [data2017, dict2017],
        2019: [data2019, dict2019],
        2022: [data2022, dict2022],
        2023: [data2023, dict2023]
    }

    def __init__(self,year):
        self.data = self.classDict[year][0]
        self.labels = self.classDict[year][1]

def district_data():
    years = [2005, 2007, 2009, 2012, 2013, 2015, 2017, 2019, 2022, 2023]

    census_data = pd.DataFrame()

    for year in years:
        survey = ACS(year)
        url = "https://api.census.gov/data/" + str(year) + "/acs/acs1/profile?get=NAME," + survey.data + "&for=congressional district:*&key=" + api_key
        response = requests.get(url)
        data = response.json()

        df = pd.DataFrame(data[1:], columns=data[0])  # Create DataFrame and drop the first row
        df = df.rename(columns=survey.labels)
        df['year'] = year

        df['median_age'] = df['median_age'].astype(float)
        df['bachelors_degree'] = df['bachelors_degree'].astype(float)
        df['latino'] = df['latino'].astype(float)
        df['white'] = df['white'].astype(float)
        df['black'] = df['black'].astype(float)
        df['native'] = df['native'].astype(float)
        df['asian'] = df['asian'].astype(float)

        if(year == 2005):
            df['total_pop'] = df['total_pop'].astype(float)

            df['latino'] = ((df['latino'] / df['total_pop']) * 100).round(1)
            df['white'] = ((df['white'] / df['total_pop']) * 100).round(1)
            df['black'] = ((df['black'] / df['total_pop']) * 100).round(1)
            df['native'] = ((df['native'] / df['total_pop']) * 100).round(1)
            df['asian'] = ((df['asian'] / df['total_pop']) * 100).round(1)

            df = df.drop(['total_pop'], axis=1)

        df = df.rename(columns={'congressional district':'district'})

        census_data = pd.concat([census_data, df])

    return census_data

def text_processing(df):
    df['state'] = df['NAME'].str.extract(r',\s([A-Za-z\s]+)$')

    state_abbr = {
        'Alabama': 'AL', 'Alaska':'AK', 'Arizona':'AZ', 'Arkansas':'AR', 'California':'CA', 'Colorado':'CO', 
        'Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA', 'Hawaii':'HI','Idaho':'ID','Illinois':'IL',
        'Indiana':'IN', 'Iowa':'IA', 'Kansas':'KS', 'Kentucky':'KY', 'Louisiana':'LA', 'Maine':'ME', 'Maryland':'MD',
        'Massachusetts':'MA', 'Michigan':'MI', 'Minnesota':'MN', 'Mississippi':'MS', 'Missouri':'MO', 'Montana':'MT',
        'Nebraska':'NE', 'Nevada':'NV', 'New Hampshire':'NH', 'New Jersey':'NJ', 'New Mexico':'NM','New York':'NY', 'North Carolina':'NC',
        'North Dakota':'ND', 'Ohio':'OH', 'Oklahoma':'OK', 'Oregon':'OR', 'Pennsylvania':'PA', 'Rhode Island':'RI', 
        'South Carolina':'SC', 'South Dakota':'SD', 'Tennessee':'TN', 'Texas':'TX', 'Utah':'UT', 'Vermont':'VT',
        'Virginia':'VA', 'Washington':'WA', 'West Virginia':'WV', 'Wisconsin':'WI', 'Wyoming':'WY'
    }

    df['state'] = df['state'].map(state_abbr)
    df = df.drop(['NAME'], axis = 1)
    df = df.dropna(subset=['state'])

    return df

def year_processing(df):
    duplicate_2005 = df[df['year'] == 2005]
    duplicate_2005['year'] = duplicate_2005['year'] - 1

    df['year'] = df['year'].apply(lambda x: x+1 if x not in [2012, 2022] else x)

    df = pd.concat([df, duplicate_2005], axis = 0)

    return df

def get_census_data():
    base = district_data()
    text = text_processing(base)
    final_data = year_processing(text)

    return final_data
