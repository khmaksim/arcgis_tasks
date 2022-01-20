import arcpy

# Возвращает объект с max значением абсолютной высоты или относительной высоты
def get_highest_object(table, id_list):
	row_selected = []

	for row in table:
		if row[0] in id_list:
			row_selected.append(row)
	row_selected = sorted(row_selected, key=lambda x: (x[1], x[2]))
	return row_selected[-1][0]

# set workspace environment
arcpy.env.workspace = "G:/projects/ArcGis/clustering/temp/SHP/New shp/Prep"
arcpy.env.overwriteOutput = True

# set variables
in_features = "prep"
near_features = "prep"

# Make a layer from the feature class
arcpy.MakeFeatureLayer_management(in_features, "lyr") 

# Within selected features, further select only those cities which have a population > 10,000   
arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", ' "FID" < 1000 ')
 
# Write the selected features to a new featureclass
arcpy.CopyFeatures_management("lyr", "prep_1000")

# arcpy.TableSelect_analysis(in_features, select_table, '"FID" < 1000')

select_table = "prep_1000"
near_select_table = "prep_1000"
search_radius = "2000"
prep_radius = "prep_distance"

# find locations within the search radius
arcpy.PointDistance_analysis(select_table, near_select_table, prep_radius, search_radius)
arcpy.AddField_management(prep_radius, "is_delete" , "SHORT", 1)

rows_prep_table = {}

with arcpy.da.SearchCursor(in_features, ['FID', 'Habs', 'Hpre']) as cursor:
	for row in cursor:
		rows_prep_table[row[0]] = (row[1], row[2])
	del row
del cursor

fids_selected = {}
num_row_order = []

with arcpy.da.UpdateCursor(prep_radius, ['INPUT_FID', 'NEAR_FID']) as cursor:
	input_fid = -1
	max_height_abs = 0
	max_height_pre = 0
	fid_near_selected = -1
	
	num_sel = -1
	num_cur = 0
	for row in cursor:
		if input_fid == row[0]:
			height_abs = rows_prep_table[row[1]][0]
			height_pre = rows_prep_table[row[1]][1]
			
			if height_abs > max_height_abs:
				max_height_abs = height_abs
				max_height_pre = height_pre
				# fid_near_selected = row[1]
				num_sel = num_cur
			elif height_abs == max_height_abs:
				if height_pre > max_height_pre:
					max_height_abs = height_abs
					max_height_pre = height_pre
					# fid_near_selected = row[1]
					num_sel = num_cur

		elif input_fid != row[0]:
			if num_sel != -1:
				num_row_order.append(num_sel)

			input_fid = row[0]
			max_height_abs = rows_prep_table[input_fid][0]
			max_height_pre = rows_prep_table[input_fid][1]
			num_sel = num_cur
		num_cur = num_cur + 1
	del row
del cursor

with arcpy.da.UpdateCursor(prep_radius, ['is_delete']) as cursor:
	num = 0
	for row in cursor:
		if num in num_row_order:
			row[0] = 0
			cursor.updateRow(row)
		num = num + 1
	del row
del cursor

result_table = "prep_res.dbf"
tempTableView = "TableView"
arcpy.MakeTableView_management(prep_radius, tempTableView)
arcpy.SelectLayerByAttribute_management(tempTableView, "NEW_SELECTION", ' "is_delete" IS NULL ')
arcpy.DeleteRows_management(tempTableView)