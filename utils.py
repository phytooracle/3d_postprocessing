import numpy as np
import csv
import open3d as o3d
from pyproj import Proj,transform
proj_4326 = Proj(init='epsg:4326')
proj_2151 = Proj(init='epsg:2152')

def load_pcd(path):
    pcd = o3d.io.read_point_cloud(path,format="ply")
    return pcd

def utm_to_latlon(easting, northing):
    lon, lat = transform(proj_2151,proj_4326,easting,northing)
    return lon,lat

def latlon_to_utm(lon,lat):
    easting,northing = transform(proj_4326,proj_2151,lon,lat)
    return easting,northing

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
    color1 = (255/255, 255/255, 0)
    color2 = (170/255, 0, 0)

    pcd.paint_uniform_color([1,1,1])
    points = np.array(pcd.points)

    mins = np.min(points,axis=0)
    maxs = np.max(points,axis=0)

    ratios = (points[:,2]-mins[2])/(maxs[2]-mins[2])
    ratios = np.vstack((ratios,ratios,ratios)).T
    colors = np.array((ratios*color1+(1-ratios)*color2))

    min_x,min_y = utm_to_latlon(mins[0],mins[1])
    max_x,max_y = utm_to_latlon(maxs[0],maxs[1])

    tree = o3d.geometry.KDTreeFlann(pcd)

    for p in plants:
        if p[0]>min_x and p[0]<max_x and p[1]>min_y and p[1]<max_y:
            utm_p = latlon_to_utm(p[0],p[1])
            [k, idx, _] = tree.search_radius_vector_3d((utm_p[0],utm_p[1],(mins[2]+maxs[2])/2),0.15)
            colors[idx] = [0,1,0]

    pcd.colors = o3d.utility.Vector3dVector(colors)

    return pcd
    

def load_plants(plants_path):
    plants=[]

    with open(plants_path, mode='r') as infile:
        reader = csv.reader(infile)
        for rows in reader:
            if rows[0] == "date":
                continue

            if float(rows[1])<0.95:
                continue

            p = [float(rows[4]),float(rows[5])]
            plants.append(p)
    
    return plants