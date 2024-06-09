# 3D Postprocessing
This script corrects geocoordinates of PLY files after they are merged and aligned and GCPs have been selected by the users manually. 

## Inputs
CSV containing clustered plant detections of an entire season.

The input CSV should have columns in the following order:
- Unnamed: 0
- plant_name
- date (Must be in format "YYYY-MM-DD")
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

## Outputs
Subdirectories containg postprocessed 3D point clouds. 

## Arguments and Flags
* **Required Arguments:**
  * **Input directory containing point clouds:** '-i', '--input'
  * **Output directory:** '-o', '--output'
  * **Folder name to be processed:** '-f', '--folder'
  * **Transformation JSON file:** '-t', '--transformation'
  * **Path to CSV file containing clustered plant detection:** '-p', '--plants'
  * **Season number:** '-s', '--season'
  * **Date of data collection:** '-d', '--date'
  * **Coordinates of GCP lids:** '-l', '--lids'
 
