SELECT rt.txt_desig, point_st.txt_name || '-' || point_nx.txt_name, 
rts.val_mag_track, rts.val_revers_mag_track,
ct_lw.txt_code || rts.val_dist_ver_upper, 
ct_up.txt_code || rts.val_dist_ver_lower,
ROUND(rts.val_len, 0), geo_b.txt_code 
FROM en_route_rte as rt 
LEFT JOIN rte_seg_m as rts ON rt.id = rts.route 
LEFT JOIN significant_point as point_st ON point_st.id = rts.start 
LEFT JOIN significant_point as point_nx ON point_nx.id = rts.next 
LEFT JOIN "CATALOG" as ct_lw ON rts.uom_dist_ver_lower = ct_lw.id 
LEFT JOIN "CATALOG" as ct_up ON rts.uom_dist_ver_upper = ct_up.id 
LEFT JOIN "GEO_BORDER" as geo_b ON geo_b.id = rts.border