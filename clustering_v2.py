import arcpy

# set workspace environment
arcpy.env.workspace = "C:/Users/kolobok/projects/python/Aviacominfo/ArcGis/cluster/BASE.gdb"
arcpy.env.overwriteOutput = True

# in_table = "prep"
# out_table = "prep_dist"
# where_clause = '"NEAR_DIST" <= 2000'
# arcpy.TableSelect_analysis(in_table, out_table, where_clause)

# set local variables
source_dataset = "obstcl"
sort_source_dataset = "obstcl_sort"

sort_fields = [["FID_pol_klusters", "ASCENDING"],]
# Use Peano algorithm
sort_method = "PEANO"

# execute the function
arcpy.Sort_management(source_dataset, sort_source_dataset, sort_fields, sort_method)
    
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

objects_id = []

with arcpy.da.SearchCursor(sort_source_dataset, ['OBJECTID', 'Habs', 'Hpre', 'FID_pol_klusters']) as cursor:
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

print(len(num_row_order))
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


result_table = "prep_res.dbf"
tempTableView = "TableView"
arcpy.MakeTableView_management(out_table, tempTableView)
arcpy.SelectLayerByAttribute_management(tempTableView, "NEW_SELECTION", "[is_delete] = '0'")