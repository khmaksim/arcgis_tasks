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

# in_table = "prep"
# out_table = "prep_dist"
# where_clause = '"NEAR_DIST" <= 2000'
# arcpy.TableSelect_analysis(in_table, out_table, where_clause)

# set variables

in_features = "prep"
near_features = "prep"
out_table = "prep_tab"
search_radius = "2000"
  
# find locations within the search radius
arcpy.PointDistance_analysis(in_features, near_features, out_table, search_radius)
arcpy.AddField_management(out_table, "is_delete" , "SHORT", 1)

# in_join_field = "NEAR_FID"
# join_table = "prep"
# join_field = "FID"
# fields = ["Habs", "Hpre"]

# Join two feature classes by the zonecode field and only carry 
# over the land use and land cover fields
# arcpy.JoinField_management(out_table, in_join_field, join_table, join_field, fields)

# result_table = "prep.dbf"
# arcpy.MakeTableView_management(result_table, out_table)

# prev_row = None
# max_Habs = 0
# max_Hpre = 0

# rows_prep_table = []

# with arcpy.da.SearchCursor(in_features, ['FID', 'Habs', 'Hpre']) as cursor:
# 		for row in cursor:
# 			rows_prep_table.append(row)

# fid_selected = []

# with arcpy.da.UpdateCursor(out_table, ['INPUT_FID', 'NEAR_FID', 'is_delete']) as cursor:
# 	input_fid = -1
# 	near_fid_list = []
# 	i = 0
# 	for row in cursor:
# 		if i == 100:
# 			break
# 		if input_fid == row[0]:
# 			near_fid_list.append(row[1])
# 		elif input_fid != row[0]:
# 			if len(near_fid_list) > 0:
# 				fid_with_max_height = get_highest_object(rows_prep_table, near_fid_list)
# 				fid_selected.append((input_fid, fid_with_max_height))
# 				near_fid_list = []
# 			if input_fid == -1:
# 				near_fid_list.append(row[1])
# 			input_fid = row[0]
# 		i = i + 1

rows_prep_table = {}

with arcpy.da.SearchCursor(in_features, ['FID', 'Habs', 'Hpre']) as cursor:
	for row in cursor:
		rows_prep_table[row[0]] = (row[1], row[2])
	del row
del cursor

fids_selected = {}
num_row_order = []

with arcpy.da.UpdateCursor(out_table, ['INPUT_FID', 'NEAR_FID']) as cursor:
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
			# if fid_near_selected != -1:
				# fids_selected[input_fid] = fid_near_selected
				num_row_order.append(num_sel)

			input_fid = row[0]
			max_height_abs = rows_prep_table[input_fid][0]
			max_height_pre = rows_prep_table[input_fid][1]
			# fid_near_selected = row[1]
			num_sel = num_cur
		num_cur = num_cur + 1
	del row
del cursor

print(len(num_row_order))

# with arcpy.da.UpdateCursor(out_table, ['INPUT_FID', 'NEAR_FID', 'is_delete']) as cursor:
# 	for row in cursor:
# 		fid_row = row[0]
# 		fid_near_row = row[1]

# 		for fid, fid_near in fids_selected.items():
# 			if fid == fid_row and fid_near == fid_near_row:
# 				fids_selected.pop(fid)
# 				continue

# 		row[2] = 1
# 		cursor.updateRow(row)
# 	del row
# del cursor

with arcpy.da.UpdateCursor(out_table, ['is_delete']) as cursor:
	num = 0
	for row in cursor:
		if num in num_row_order:
			row[0] = 0
			cursor.updateRow(row)
		num = num + 1
	del row
del cursor


	# for row in cursor:
	# 	if input_fid == row[0]:
	# 		if max_Habs > row[2]:
	# 			row[4] = 1
	# 			cursor.updateRow(row)
	# 		elif max_Habs < row[2]:
	# 			prev_row[4] = 1
	# 			cursor.updateRow(prev_row)
	# 			max_Habs = row[2]
	# 			max_Hpre = row[3]
	# 			prev_row = row
	# 		elif max_Hpre > row[3]:
	# 			row[4] = 1
	# 			cursor.updateRow(row)
	# 		elif max_Hpre < row[3]:
	# 			prev_row[4] = 1
	# 			cursor.updateRow(prev_row)
	# 			max_Habs = row[2]
	# 			max_Hpre = row[3]
	# 			prev_row = row
	# 		else:
	# 			row[4] = 1
	# 			cursor.updateRow(row)
	# 	elif input_fid != row[0]:
	# 		prev_row = row
	# 		input_fid = row[0]
	# 		max_Habs = row[2]
	# 		max_Hpre = row[3]

result_table = "prep_res.dbf"
tempTableView = "TableView"
arcpy.MakeTableView_management(out_table, tempTableView)
arcpy.SelectLayerByAttribute_management(tempTableView, "NEW_SELECTION", "[is_delete] = '0'")