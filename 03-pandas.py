import pandas as pd

wd = '/Volumes/Echo/GIS/projects/vosd/tasks/201406_transit_pop/data/'

wt = wd+'tables/intersect/'

buf_dist = ['1320','2640']
buf_dist_txt = ['025','050']

inCensus = ['acs_5y_2012_bg','acs_5y_2012_ct','census_2010_bl']
areaCensus = ['bg2012areasqmeter','ct2012areasqmeter','bl2010areasqmeter']
popField = ['bg2012pop','ct2012pop','bl2010pop']

for h in buf_dist_txt:
	for i, j, k in zip(inCensus,areaCensus,popField):
		inFile = wt + "trolley_"+h+"mile_"+i+"_int_dis_raw.csv"
		outFile= wt + "trolley_"+h+"mile_"+i+"_int_dis.csv"
		df = pd.read_csv(inFile)
		df = df[['stop_id','SUM_'+k+'_int_'+h]]
		df[k+'buf'+h+'miles'] = df['SUM_'+k+'_int_'+h]
		df = df.drop('SUM_'+k+'_int_'+h, axis=1)
		df.to_csv(outFile, index=False)

mFile = wd + 'input/trolley_locations/trolley_xy.csv'

df = pd.read_csv(mFile)

for h in buf_dist_txt:
	for i, j, k in zip(inCensus,areaCensus,popField):
		inFile= wt + "trolley_"+h+"mile_"+i+"_int_dis.csv"
		t = pd.read_csv(inFile)
		df = df.merge(t, on='stop_id')

outFile1= wd + 'tables/trolley_pop_estimates.csv'
outFile2= '/Users/danielmsheehan/GitHub/pop_estimate/data/trolley_pop_estimates.csv'
df.to_csv(outFile1, index=False)
df.to_csv(outFile2, index=False)

