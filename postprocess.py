import os
import json
from utils import *

def get_path_dict(path,outpath,folder_name):
    if path[-1] == '/':
        path = path[:-1]
    
    pass_id = os.listdir(os.path.join(path,"east",folder_name))[0].split('/')[-1].split('_')[0]

    east_path = os.path.join(path,"east",folder_name)
    east_downsampled_path = os.path.join(path,"east_downsampled",folder_name)
    west_path = os.path.join(path,"west",folder_name)
    west_downsampled_path = os.path.join(path,"west_downsampled",folder_name)
    merged_path = os.path.join(path,"merged",folder_name)
    merged_downsampled_path = os.path.join(path,"merged_downsampled",folder_name)

    east_outpath = os.path.join(outpath,"east",folder_name)
    east_downsampled_outpath = os.path.join(outpath,"east_downsampled",folder_name)
    west_outpath = os.path.join(outpath,"west",folder_name)
    west_downsampled_outpath = os.path.join(outpath,"west_downsampled",folder_name)
    merged_outpath = os.path.join(outpath,"merged",folder_name)
    merged_downsampled_outpath = os.path.join(outpath,"merged_downsampled",folder_name)

    os.makedirs(east_outpath,exist_ok=True)
    os.makedirs(east_downsampled_outpath,exist_ok=True)
    os.makedirs(west_outpath,exist_ok=True)
    os.makedirs(west_downsampled_outpath,exist_ok=True)
    os.makedirs(merged_outpath,exist_ok=True)
    os.makedirs(merged_downsampled_outpath,exist_ok=True)

    aligned_ply_path = os.path.join(merged_path,f"{pass_id}__Top-heading-merged.ply")
    aligned_downsampled_ply_path = os.path.join(merged_downsampled_path,f"{pass_id}__Top-heading-merged.ply")
    aligned_east_path = os.path.join(east_path,f"{pass_id}__Top-heading-east.ply")
    aligned_west_path = os.path.join(west_path,f"{pass_id}__Top-heading-west.ply")
    aligned_east_downsampled_path = os.path.join(east_downsampled_path,f"{pass_id}__Top-heading-east.ply")
    aligned_west_downsampled_path = os.path.join(west_downsampled_path,f"{pass_id}__Top-heading-west.ply")

    geocorrected_east_path = os.path.join(east_outpath,f"{pass_id}__Top-heading-east.ply")
    geocorrected_west_path = os.path.join(west_outpath,f"{pass_id}__Top-heading-west.ply")
    geocorrected_east_downsampled_path = os.path.join(east_downsampled_outpath,f"{pass_id}__Top-heading-east.ply")
    geocorrected_west_downsampled_path = os.path.join(west_downsampled_outpath,f"{pass_id}__Top-heading-west.ply")
    geocorrected_ply_path = os.path.join(merged_outpath,f"{pass_id}__Top-heading-merged.ply")
    geocorrected_downsampled_ply_path = os.path.join(merged_downsampled_outpath,f"{pass_id}__Top-heading-merged.ply")

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

def postprocess_single_pass(path,outpath,folder,plant_path,transformation,season,current_date,lid_path):
    with open(transformation,'r') as f:
        tr = json.load(f)

    T = np.array(tr['transformation'])

    plants = load_plants(plant_path,season,current_date)
    lids = load_lids(lid_path)
    path_dict = get_path_dict(path,outpath,folder)
    
    pcd = load_pcd(path_dict['aligned_downsampled_ply_path'])
    transformed_pcd = transform_pcd(pcd,T)
    painted_pcd = paint_plants(transformed_pcd,plants)
    painted_pcd = paint_lids(painted_pcd,lids)
    save_pcd(painted_pcd,path_dict['geocorrected_downsampled_ply_path'])

    pcd = load_pcd(path_dict['aligned_ply_path'])
    transformed_pcd = transform_pcd(pcd,T)
    painted_pcd = paint_plants(transformed_pcd,plants)
    painted_pcd = paint_lids(painted_pcd,lids)
    save_pcd(painted_pcd,path_dict['geocorrected_ply_path'])

    pcd = load_pcd(path_dict['aligned_east_path'])
    transformed_pcd = transform_pcd(pcd,T)
    painted_pcd = paint_plants(transformed_pcd,plants)
    painted_pcd = paint_lids(painted_pcd,lids)
    save_pcd(painted_pcd,path_dict['geocorrected_east_path'])

    pcd = load_pcd(path_dict['aligned_west_path'])
    transformed_pcd = transform_pcd(pcd,T)
    painted_pcd = paint_plants(transformed_pcd,plants)
    painted_pcd = paint_lids(painted_pcd,lids)
    save_pcd(painted_pcd,path_dict['geocorrected_west_path'])

    pcd = load_pcd(path_dict['aligned_east_downsampled_path'])
    transformed_pcd = transform_pcd(pcd,T)
    painted_pcd = paint_plants(transformed_pcd,plants)
    painted_pcd = paint_lids(painted_pcd,lids)
    save_pcd(painted_pcd,path_dict['geocorrected_east_downsampled_path'])

    pcd = load_pcd(path_dict['aligned_west_downsampled_path'])
    transformed_pcd = transform_pcd(pcd,T)
    painted_pcd = paint_plants(transformed_pcd,plants)
    painted_pcd = paint_lids(painted_pcd,lids)
    save_pcd(painted_pcd,path_dict['geocorrected_west_downsampled_path'])
