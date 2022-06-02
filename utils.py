import pdb
import numpy as np
import csv
import open3d as o3d
from datetime import datetime
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

def load_lids(path):
    lids = {}
    with open(path, mode='r') as infile:
        reader = csv.reader(infile)
        for rows in reader:
            p = [float(rows[1]),float(rows[2])]
            p = latlon_to_utm(p[1],p[0])
            lids[int(float(rows[0]))] = [p[0],p[1]]
    return lids

def paint_lids(pcd,lids):
    points = np.array(pcd.points)

    mins = np.min(points,axis=0)
    maxs = np.max(points,axis=0)

    min_x,min_y = mins[0],mins[1]
    max_x,max_y = maxs[0],maxs[1]

    tree = o3d.geometry.KDTreeFlann(pcd)
    colors = np.array(pcd.colors)

    for l in lids:
        p = lids[l]
        if p[0]>min_x and p[0]<max_x and p[1]>min_y and p[1]<max_y:
            utm_p = p
            [k, idx, _] = tree.search_radius_vector_3d((utm_p[0],utm_p[1],(mins[2]+maxs[2])/2),0.3)
            colors[idx] = [0,0,1]

    pcd.colors = o3d.utility.Vector3dVector(colors)

    return pcd

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
    

def keep_closest_date_plants(all_plants,date):

    all_dates = [datetime(int(k.split('-')[0]),int(k.split('-')[1]),int(k.split('-')[2])) for k in all_plants]
    current_date = datetime(int(date.split('-')[0]),int(date.split('-')[1]),int(date.split('-')[2]))

    res = min(all_dates, key=lambda sub: abs(sub - current_date))

    return all_plants[res.strftime("%Y-%m-%d")]
    

def load_plants(plants_path,season,current_date):

    if season == 10:
        
        all_plants = {}
        with open(plants_path, mode='r' ,encoding="utf-8") as infile:
            reader = csv.reader(infile)
            for rows in reader:
                if rows[2] == "date":
                    continue
                
                if rows[2] == "2020-03-02":
                    continue
                
                p = [float(rows[6]),float(rows[7])]
                date = rows[2]

                if date not in all_plants:
                    all_plants[date] = [p]
                else:
                    all_plants[date].append(p)

    else:

        all_plants = {}
        with open(plants_path, mode='r') as infile:
            reader = csv.reader(infile)
            for rows in reader:
                if rows[2] == "date":
                    continue

                p = [float(rows[5]),float(rows[6])]
                date = rows[2]

                if date not in all_plants:
                    all_plants[date] = [p]
                else:
                    all_plants[date].append(p)

    plants = keep_closest_date_plants(all_plants,current_date)
    
    return plants
