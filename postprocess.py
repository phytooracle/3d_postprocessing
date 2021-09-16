import os
import json
from utils import *

def get_path_dict(path,outpath):
    if path[-1] == '/':
        path = path[:-1]
    
    pass_id = os.listdir(path)[0].split('/')[-1].split('_')[0]
    folder_name = path.split('/')[-1]
    
    if folder_name not in outpath:
        outpath = os.path.join(outpath,folder_name)
        if not os.path.exists(outpath):
            os.mkdir(outpath)

    aligned_ply_path = os.path.join(path,f"{pass_id}__Top-heading-aligned.ply")
    aligned_downsampled_ply_path = os.path.join(path,f"{pass_id}__Top-heading-aligned-downsampled.ply")
    aligned_east_path = os.path.join(path,f"{pass_id}__Top-heading-aligned_east.ply")
    aligned_west_path = os.path.join(path,f"{pass_id}__Top-heading-aligned_west.ply")
    aligned_east_downsampled_path = os.path.join(path,f"{pass_id}__Top-heading-aligned_east_downsampled.ply")
    aligned_west_downsampled_path = os.path.join(path,f"{pass_id}__Top-heading-aligned_west_downsampled.ply")

    geocorrected_ply_path = os.path.join(outpath,f"{pass_id}__Top-heading-geocorrected.ply")
    geocorrected_downsampled_ply_path = os.path.join(outpath,f"{pass_id}__Top-heading-geocorrected-downsampled.ply")
    geocorrected_east_path = os.path.join(outpath,f"{pass_id}__Top-heading-geocorrected_east.ply")
    geocorrected_west_path = os.path.join(outpath,f"{pass_id}__Top-heading-geocorrected_west.ply")
    geocorrected_east_downsampled_path = os.path.join(outpath,f"{pass_id}__Top-heading-geocorrected_east_downsampled.ply")
    geocorrected_west_downsampled_path = os.path.join(outpath,f"{pass_id}__Top-heading-geocorrected_west_downsampled.ply")

    path_dict = {}
    path_dict['aligned_ply_path'] = aligned_ply_path
    path_dict['aligned_downsampled_ply_path'] = aligned_downsampled_ply_path
    path_dict['aligned_east_path'] = aligned_east_path
    path_dict['aligned_west_path'] = aligned_west_path
    path_dict['aligned_east_downsampled_path'] = aligned_east_downsampled_path
    path_dict['aligned_west_downsampled_path'] = aligned_west_downsampled_path

    path_dict['geocorrected_ply_path'] = geocorrected_ply_path
    path_dict['geocorrected_downsampled_ply_path'] = geocorrected_downsampled_ply_path
    path_dict['geocorrected_east_path'] = geocorrected_east_path
    path_dict['geocorrected_west_path'] = geocorrected_west_path
    path_dict['geocorrected_east_downsampled_path'] = geocorrected_east_downsampled_path
    path_dict['geocorrected_west_downsampled_path'] = geocorrected_west_downsampled_path

    path_dict['pass_id'] = pass_id
    path_dict['folder_name'] = folder_name

    return path_dict

def postprocess_single_pass(path,outpath,plant_path,transformation):
    # T = np.array([[9.83721793e-04,5.35915882e-06,4.08975685e+05],[2.80464642e-06,9.36477094e-04,3.65996821e+06]])
    T = np.array(eval(transformation))

    plants = load_plants(plant_path)
    path_dict = get_path_dict(path,outpath)
    
    pcd = load_pcd(path_dict['aligned_downsampled_ply_path'])
    transformed_pcd = transform_pcd(pcd,T)
    painted_pcd = paint_plants(transformed_pcd,plants)
    save_pcd(painted_pcd,path_dict['geocorrected_downsampled_ply_path'])

    pcd = load_pcd(path_dict['aligned_ply_path'])
    transformed_pcd = transform_pcd(pcd,T)
    painted_pcd = paint_plants(transformed_pcd,plants)
    save_pcd(painted_pcd,path_dict['geocorrected_ply_path'])

    pcd = load_pcd(path_dict['aligned_east_path'])
    transformed_pcd = transform_pcd(pcd,T)
    painted_pcd = paint_plants(transformed_pcd,plants)
    save_pcd(painted_pcd,path_dict['geocorrected_east_path'])

    pcd = load_pcd(path_dict['aligned_west_path'])
    transformed_pcd = transform_pcd(pcd,T)
    painted_pcd = paint_plants(transformed_pcd,plants)
    save_pcd(painted_pcd,path_dict['geocorrected_west_path'])

    pcd = load_pcd(path_dict['aligned_east_downsampled_path'])
    transformed_pcd = transform_pcd(pcd,T)
    painted_pcd = paint_plants(transformed_pcd,plants)
    save_pcd(painted_pcd,path_dict['geocorrected_east_downsampled_path'])

    pcd = load_pcd(path_dict['aligned_west_downsampled_path'])
    transformed_pcd = transform_pcd(pcd,T)
    painted_pcd = paint_plants(transformed_pcd,plants)
    save_pcd(painted_pcd,path_dict['geocorrected_west_downsampled_path'])
