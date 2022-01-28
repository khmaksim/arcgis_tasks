SELECT rt.txt_desig, COALESCE(point_st.txt_name, ''), COALESCE(point_nx.txt_name, ''), COALESCE(rts.val_mag_track, 0), COALESCE(rts.val_revers_mag_track, 0),
COALESCE(ct_lw.txt_code, ''), COALESCE(rts.val_dist_ver_upper, 0), COALESCE(ct_up.txt_code, ''), COALESCE(rts.val_dist_ver_lower, 0),
ROUND(COALESCE(rts.val_len, 0), 0), COALESCE(geo_b.txt_code, '') 
FROM en_route_rte as rt 
LEFT JOIN rte_seg_m as rts ON rt.id = rts.route 
LEFT JOIN significant_point as point_st ON point_st.id = rts.start 
LEFT JOIN significant_point as point_nx ON point_nx.id = rts.next 
LEFT JOIN "CATALOG" as ct_lw ON rts.uom_dist_ver_lower = ct_lw.id 
LEFT JOIN "CATALOG" as ct_up ON rts.uom_dist_ver_upper = ct_up.id 
LEFT JOIN "GEO_BORDER" as geo_b ON geo_b.id = rts.border