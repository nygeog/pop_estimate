import arcpy, time, datetime, csv, sys, traceback
from arcpy import env
env.overwriteOutput = True

wd = "V:/GIS/projects/vosd/tasks/201406_transit_pop/data/"

# just raw census geo, don't need
# print 'copy tract 2010 shape'
# arcpy.Select_analysis("W:/GIS/Data/Census/census_2010/tracts/census.gdb/tracts_2010",wd+"input/input.gdb/tracts_2010",""""STATEFP10" = '06' AND "COUNTYFP10" = '073'""")
print 'bring in csv'
arcpy.TableToTable_conversion(wd+"input/trolley_locations/trolley_xy.csv",wd+"input/input.gdb","trolley_xy")
print 'make xy event layer in wgs 84 (temporary)'
arcpy.MakeXYEventLayer_management(wd+"input/input.gdb/trolley_xy","stop_lon","stop_lat","trolley_xy_Layer","GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision","#")
print 'project to cali state plane zone 6 (nad 83) feet - maybe consider UTM Z 11N if SD published data is that proj. sys.'
arcpy.Project_management("trolley_xy_Layer",wd+"input/input.gdb/trolley_locations","PROJCS['NAD_1983_StatePlane_California_VI_FIPS_0406_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',6561666.666666666],PARAMETER['False_Northing',1640416.666666667],PARAMETER['Central_Meridian',-116.25],PARAMETER['Standard_Parallel_1',32.78333333333333],PARAMETER['Standard_Parallel_2',33.88333333333333],PARAMETER['Latitude_Of_Origin',32.16666666666666],UNIT['Foot_US',0.3048006096012192]]","WGS_1984_(ITRF00)_To_NAD_1983","GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433],METADATA['World',-180.0,-90.0,180.0,90.0,0.0,0.0174532925199433,0.0,1262]]")

print 'copy acs 2008-2012 block group'
arcpy.Select_analysis("W:/GIS/Data/Census/acs_2008_2012/block_group/ACS_2012_5YR_BG_06_CALIFORNIA.gdb/ACS_2012_5YR_BG_06_CALIFORNIA",wd+"input/input.gdb/acs_5y_2012_bg",""""COUNTYFP" = '073'""")
arcpy.Project_management(wd+"input/input.gdb/acs_5y_2012_bg",wd+"input/input.gdb/acs_5y_2012_bg_prj","PROJCS['NAD_1983_StatePlane_California_VI_FIPS_0406_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',6561666.666666666],PARAMETER['False_Northing',1640416.666666667],PARAMETER['Central_Meridian',-116.25],PARAMETER['Standard_Parallel_1',32.78333333333333],PARAMETER['Standard_Parallel_2',33.88333333333333],PARAMETER['Latitude_Of_Origin',32.16666666666666],UNIT['Foot_US',0.3048006096012192]]","#","GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433],METADATA['North America - NAD83',167.65,14.93,-47.74,86.45,0.0,0.0174532925199433,0.0,1350]]")
arcpy.TableToTable_conversion("W:/GIS/Data/Census/acs_2008_2012/block_group/ACS_2012_5YR_BG_06_CALIFORNIA.gdb/X01_AGE_AND_SEX",wd+"input/input.gdb","acs_5y_2012_bg_counts")
print 'copy acs 2008-2012 tract'
arcpy.Select_analysis("W:/GIS/Data/Census/acs_2008_2012/tract/ACS_2012_5YR_TRACT_06_CALIFORNIA.gdb/ACS_2012_5YR_TRACT_06_CALIFORNIA",wd+"input/input.gdb/acs_5y_2012_ct",""""COUNTYFP" = '073'""")
arcpy.Project_management(wd+"input/input.gdb/acs_5y_2012_ct",wd+"input/input.gdb/acs_5y_2012_ct_prj","PROJCS['NAD_1983_StatePlane_California_VI_FIPS_0406_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',6561666.666666666],PARAMETER['False_Northing',1640416.666666667],PARAMETER['Central_Meridian',-116.25],PARAMETER['Standard_Parallel_1',32.78333333333333],PARAMETER['Standard_Parallel_2',33.88333333333333],PARAMETER['Latitude_Of_Origin',32.16666666666666],UNIT['Foot_US',0.3048006096012192]]","#","GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433],METADATA['North America - NAD83',167.65,14.93,-47.74,86.45,0.0,0.0174532925199433,0.0,1350]]")
arcpy.TableToTable_conversion("W:/GIS/Data/Census/acs_2008_2012/tract/ACS_2012_5YR_TRACT_06_CALIFORNIA.gdb/X01_AGE_AND_SEX",wd+"input/input.gdb","acs_5y_2012_ct_counts")
print 'copy census 2010 block'
arcpy.Select_analysis("W:/GIS/Data/Census/census_2010/blocks/tabblock2010_06_pophu/tabblock2010_06_pophu.shp",wd+"input/input.gdb/census_2010_bl",""""COUNTYFP10" = '073'""")
arcpy.Project_management(wd+"input/input.gdb/census_2010_bl",wd+"input/input.gdb/census_2010_bl_prj","PROJCS['NAD_1983_StatePlane_California_VI_FIPS_0406_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',6561666.666666666],PARAMETER['False_Northing',1640416.666666667],PARAMETER['Central_Meridian',-116.25],PARAMETER['Standard_Parallel_1',32.78333333333333],PARAMETER['Standard_Parallel_2',33.88333333333333],PARAMETER['Latitude_Of_Origin',32.16666666666666],UNIT['Foot_US',0.3048006096012192]]","#","GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433],METADATA['North America - NAD83',167.65,14.93,-47.74,86.45,0.0,0.0174532925199433,0.0,1350]]")

inCensus = ['acs_5y_2012_bg','acs_5y_2012_ct','census_2010_bl']
areaCensus = ['bg2012areasqmeter','ct2012areasqmeter','bl2010areasqmeter']

print 'add original area field'
for i, j in zip(inCensus,areaCensus):
	arcpy.AddField_management(wd+"input/input.gdb/"+i+"_prj",j,"DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
	arcpy.CalculateField_management(wd+"input/input.gdb/"+i+"_prj",j,"!shape.area@squaremeters!","PYTHON_9.3","#")

print 'join tables for counts data'
arcpy.JoinField_management(wd+"input/input.gdb/acs_5y_2012_bg_prj","GEOID_Data",wd+"input/input.gdb/acs_5y_2012_bg_counts","GEOID","B01001e1")
arcpy.JoinField_management(wd+"input/input.gdb/acs_5y_2012_ct_prj","GEOID_Data",wd+"input/input.gdb/acs_5y_2012_ct_counts","GEOID","B01001e1")

popField = ['bg2012pop','ct2012pop','bl2010pop']
orgPopField = ['B01001e1','B01001e1','POP10'] 
print 'standardize population fields'
for i, j, k in zip(inCensus,popField,orgPopField):
	arcpy.AddField_management(wd+"input/input.gdb/"+i+"_prj",j,"DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
	arcpy.CalculateField_management(wd+"input/input.gdb/"+i+"_prj",j,"!"+k+"!","PYTHON_9.3","#")

