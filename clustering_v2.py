import arcpy

# set workspace environment
arcpy.env.workspace = "C:/Users/kolobok/projects/python/Aviacominfo/ArcGis/cluster/BASE.gdb"
arcpy.env.overwriteOutput = True

# set local variables
source_dataset = "obstcl"
sort_source_dataset = "obstcl_sort"

sort_fields = [["FID_pol_klusters", "ASCENDING"],]
# Use Peano algorithm
sort_method = "PEANO"

# sort by FID_pol_klusters
arcpy.Sort_management(source_dataset, sort_source_dataset, sort_fields, sort_method)

objects_id = []

with arcpy.da.SearchCursor(sort_source_dataset, ['OBJECTID_1', 'Habs', 'Hpre', 'FID_pol_klusters']) as cursor:
	height_abs_max = 0
	height_pre_max = 0
	object_id = -1
	fid = -1

	for row in cursor:
		if fid == row[3]:
			if height_abs_max < row[1]:
				height_abs_max = row[1]
				height_pre_max = row[2]
				object_id = row[0]
			elif height_abs_max == row[1] and height_pre_max < row[2]:
				height_abs_max = row[1]
				height_pre_max = row[2]
				object_id = row[0]
			continue
		elif fid != row[3] and fid != -1:
			objects_id.append(object_id)

		object_id = row[0]
		height_abs_max = row[1]
		height_pre_max = row[2]
		fid = row[3]
	del row
del cursor

where_sql = 'OBJECTID_1 IN (' + ','.join(str(id) for id in objects_id) + ')'
arcpy.SelectLayerByAttribute_management(sort_source_dataset, "NEW_SELECTION", where_sql)
arcpy.CopyFeatures_management(sort_source_dataset, 'result')