# 3d_postprocessing
A repository for geo-correcting the ply files after they are merged and aligned and GCPs have been selected by the users manually. 

The input CSV should have columns in the following order:
- Unnamed: 0
- plant_name
- date
- treatment
- plot
- genotype
- lon
- lat
- min_x
- max_x
- min_y
- max_y
- nw_lat
- nw_lon
- se_lat
- se_lon
- bounding_area_m2
- pred_conf (OPTIONAL)
