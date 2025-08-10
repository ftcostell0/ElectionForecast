import pandas as pd

def process_cook_pvi():
    sheet_list = ['108th (03-04)', '109th (05-06)', '110th (07-08)', '111th (09-10)', '113th (13-14)', '114th (15-16)', '115th (17-18)', '116th (19-20)', '118th (23-24)']
    years = [2003, 2005, 2007, 2009, 2013, 2015, 2017, 2019, 2023]

    df = pd.DataFrame()

    for i in range(len(sheet_list)):
        sheet = sheet_list[i]
        year = years[i]

        pvi_column = str(year) + ' Cook PVI'

        temp_df = pd.read_excel('data/cook_pvi/Cook PVI 1997-2025.xlsx', sheet_name=sheet)
        temp_df = process_state_district(temp_df)
        temp_df['pvi'] = temp_df[pvi_column].apply(process_pvi)
        temp_df = process_incumbents(temp_df)
        temp_df['year'] = year + 1
        temp_df = temp_df.filter(items=['year','state', 'district', 'pvi', 'republican_incumbent', 'democratic_incumbent'])

        df = pd.concat([df, temp_df], axis=0)
        
    cycle2012 = pd.read_csv('data/cook_pvi/cycle2012.csv', index_col= 0)
    cycle2022 = pd.read_csv('data/cook_pvi/cycle2022.csv', index_col= 0)

    df = pd.concat([df, cycle2012, cycle2022], axis=0)

    df = incumbent_override(df)

    return df

def process_state_district(df):
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

    df = df.rename(columns={'District':'district', 'State':'state', 'Number':'district'})
    df['state'] = df['state'].map(state_abbr)
    df.loc[df['district'] == 'AL', 'district'] = 0
    
    return df

def process_pvi(pvi):
    if 'D+' in pvi: 
        return -int(pvi.replace('D+', ''))  
    elif 'R+' in pvi: 
        return int(pvi.replace('R+', ''))
    else:
        return 0
    
def process_incumbents(df):
    df['republican_incumbent'] = df['Party'] == 'R'
    df['democratic_incumbent'] = ~df['republican_incumbent']

    return df

def incumbent_override(df):
    retirements = pd.read_csv('data/cook_pvi/retirements.csv')

    filter_tuples = list(zip(retirements['year'], retirements['state'], retirements['district']))

    df['override'] = (df.apply(lambda row: (row['year'], row['state'], row['district']) in filter_tuples, axis=1))

    df.loc[df['override'], ['republican_incumbent', 'democratic_incumbent']] = False

    df = df.drop(columns=['override'])
    
    return df