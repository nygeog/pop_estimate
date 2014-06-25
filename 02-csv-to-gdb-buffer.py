import arcpy, time, datetime, csv, sys, traceback
from arcpy import env
env.overwriteOutput = True

wd = "V:/GIS/projects/vosd/tasks/201406_transit_pop/data/"

print 'buf dist list - just 1/2 mile'
buf_dist = ['1320','2640']
buf_dist_txt = ['025','050']

for i,j in zip(buf_dist, buf_dist_txt):
	dist = i + " Feet"
	arcpy.Buffer_analysis(wd+"input/input.gdb/trolley_locations",wd+"processing/buffers.gdb/trolley_"+j+"mile",dist,"FULL","ROUND","NONE","#")

arcpy.AddField_management(wd+"input/input.gdb/tracts_2010","ct2010areasqmeters","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.CalculateField_management(wd+"input/input.gdb/tracts_2010","ct2010areasqmeters","!shape.area@squaremeters!","PYTHON_9.3","#")

inCensus = ['acs_5y_2012_bg','acs_5y_2012_ct','census_2010_bl']
areaCensus = ['bg2012areasqmeter','ct2012areasqmeter','bl2010areasqmeter']
popField = ['bg2012pop','ct2012pop','bl2010pop']

for h in buf_dist_txt:
	for i, j, k in zip(inCensus,areaCensus,popField):
		arcpy.Intersect_analysis(wd+"processing/buffers.gdb/trolley_"+h+"mile #;"+wd+"input/input.gdb/"+i+"_prj #",wd+"processing/intersect.gdb/trolley_"+h+"mile_"+i+"_int","ALL","#","INPUT")
		arcpy.AddField_management(wd+"processing/intersect.gdb/trolley_"+h+"mile_"+i+"_int","newarea","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
		arcpy.AddField_management(wd+"processing/intersect.gdb/trolley_"+h+"mile_"+i+"_int","pctorigarea","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
		arcpy.AddField_management(wd+"processing/intersect.gdb/trolley_"+h+"mile_"+i+"_int",k+"_int_"+h,"DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
		arcpy.CalculateField_management(wd+"processing/intersect.gdb/trolley_"+h+"mile_"+i+"_int","newarea","!shape.area@squaremeters!","PYTHON_9.3","#")
		exp1 = "!newarea!/!"+j+"!"
		arcpy.CalculateField_management(wd+"processing/intersect.gdb/trolley_"+h+"mile_"+i+"_int","pctorigarea",exp1,"PYTHON_9.3","#")
		exp2 = '!'+k+'!*!pctorigarea!'
		arcpy.CalculateField_management(wd+"processing/intersect.gdb/trolley_"+h+"mile_"+i+"_int",k+"_int_"+h,exp2,"PYTHON_9.3","#")
		arcpy.AddField_management(wd+"processing/intersect.gdb/trolley_"+h+"mile_"+i+"_int","dup","LONG","#","#","#","#","NULLABLE","NON_REQUIRED","#")
		stats = k+"_int_"+h+" SUM"
		arcpy.Dissolve_management(wd+"processing/intersect.gdb/trolley_"+h+"mile_"+i+"_int",wd+"processing/intersect.gdb/trolley_"+h+"mile_"+i+"_int_dis","stop_id",stats,"MULTI_PART","DISSOLVE_LINES")

		#input table or GIS file
		table   = wd+"processing/intersect.gdb/trolley_"+h+"mile_"+i+"_int_dis"
		outfile = wd+"tables/intersect/trolley_"+h+"mile_"+i+"_int_dis_raw.csv"

		#--first lets make a list of all of the fields in the table
		fields = arcpy.ListFields(table)
		field_names = [field.name for field in fields]

		with open(outfile,'wb') as f:
		    w = csv.writer(f)
		    #--write all field names to the output file
		    w.writerow(field_names)

		    #--now we make the search cursor that will iterate through the rows of the table
		    for row in arcpy.SearchCursor(table):
		        field_vals = [row.getValue(field.name) for field in fields]
		        w.writerow(field_vals)
		    del row
		print "export population stats export is complete"