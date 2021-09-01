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
    
    geocorrected_ply_path = os.path.join(outpath,f"{pass_id}__Top-heading-geocorrected.ply")
    geocorrected_downsampled_ply_path = os.path.join(outpath,f"{pass_id}__Top-heading-geocorrected-downsampled.ply")
    
    path_dict = {}
    path_dict['aligned_ply_path'] = aligned_ply_path
    path_dict['aligned_downsampled_ply_path'] = aligned_downsampled_ply_path
    path_dict['geocorrected_ply_path'] = geocorrected_ply_path
    path_dict['geocorrected_downsampled_ply_path'] = geocorrected_downsampled_ply_path
    path_dict['pass_id'] = pass_id
    path_dict['folder_name'] = folder_name

    return path_dict

def postprocess_single_pass(path,outpath,plant_path):
    T = np.array([[9.83721793e-04,5.35915882e-06,4.08975685e+05],[2.80464642e-06,9.36477094e-04,3.65996821e+06]])
    # plants = load_plants(plant_path)
    path_dict = get_path_dict(path,outpath)
    pcd = load_pcd(path_dict['aligned_downsampled_ply_path'])
    transformed_pcd = transform_pcd(pcd,T)
    # painted_pcd = paint_plants(transformed_pcd,plants)
    save_pcd(transformed_pcd,path_dict['geocorrected_downsampled_ply_path'])
