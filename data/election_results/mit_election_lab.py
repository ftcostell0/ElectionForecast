import pandas as pd

def get_house_data():
    house_data = pd.read_csv('data/political/1976-2022-house.csv')

    house_data = house_data[house_data['year'] >= 2004]
    house_data = house_data.drop(['state', 'state_fips', 'state_cen', 'state_ic', 'office', 'stage', 'runoff', 'special', 'candidate', 'mode', 'unofficial', 'version', 'writein', 'fusion_ticket', 'totalvotes'], axis=1)

    house_data['max_votes'] = house_data.groupby(['year', 'state_po', 'district'])['candidatevotes'].transform('max')
    house_data = house_data[house_data['candidatevotes'] == house_data['max_votes']]

    house_data['republican_victory'] = (house_data['party'] == 'REPUBLICAN')
    house_data = house_data.drop(['party', 'candidatevotes', 'max_votes'], axis = 1)

    data_2024 = pd.read_csv('data/political/2024manualresults.csv')

    data_2026 = data_2024.copy()
    data_2026['year'] = 2026
    data_2026['republican_victory'] = pd.NA

    house_data = pd.concat([house_data, data_2024, data_2026])

    return house_data
