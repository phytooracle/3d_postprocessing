import numpy as np
import open3d as o3d

def load_pcd(path):
    pcd = o3d.io.read_point_cloud(path,format="ply")
    return pcd

def transform_pcd(pcd,T):
    points = np.array(pcd.points)
    z_points = np.copy(points[:,2])
    points[:,2] = 1
    transformed_points = np.matmul(T,points.T).T
    transformed_points = transformed_points[:,:2]
    transformed_points = np.hstack((transformed_points, np.expand_dims(z_points*0.001,axis=-1)))
    transformed_pcd = o3d.geometry.PointCloud() 
    transformed_pcd.points = o3d.utility.Vector3dVector(transformed_points)
    return transformed_pcd

def save_pcd(pcd,path):
    o3d.io.write_point_cloud(path, pcd)

def paint_plants(pcd,plants):
    pass

def load_plants(plants_path):
    pass