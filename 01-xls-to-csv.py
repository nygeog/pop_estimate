import pandas as pd

inFile = '/Volumes/Echo/GIS/projects/vosd/tasks/201406_transit_pop/data/input/trolley_locations/Trolley_Locations.xlsx'
outFile= '/Volumes/Echo/GIS/projects/vosd/tasks/201406_transit_pop/data/input/trolley_locations/trolley_xy.csv'
df = pd.read_excel(inFile, 'Sheet1', index_col=None, na_values=['NA'])

df.to_csv(outFile, index=False)