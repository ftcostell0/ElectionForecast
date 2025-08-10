import pandas as pd
from census import census
from cook_pvi import pvi
from election_results import mit_election_lab

census_data = census.get_census_data()
pvi_data = pvi.get_pvi_data()
election_labels = mit_election_lab.get_house_data()


df = pd.merge(election_labels, pvi_data, how='inner', on=['year', 'state', 'district'])
df = pd.merge(df, census_data, how='inner', on=['year','state','district'])
print(df)