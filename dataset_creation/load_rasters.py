#!/usr/bin/python
"""
Created on Thu Dec 27 13:37:32 2018
@author: Ziyi Gong, Samuel Konat
Version: python 3.6
"""

import psycopg2
from math import *
from osgeo import gdal
from osgeo import osr
from affine import Affine
import sys
import os

R = 6371        # Radius of the Earth
GS = [64]       # Grid sizes in pixels

orgLoc = '/home/ubuntu/kynesfield/datasets/original'
cpdLoc = '/home/ubuntu/kynesfield/datasets/clipped'

# Database details
dbhost = "localhost"
dbname = "postgres"
dbuser = "postgres"
dbpass = "kynes"
dbconn = None

# Translation variables
IN = osr.SpatialReference()
IN.ImportFromEPSG(4326)
OUT = osr.SpatialReference()
OUT.ImportFromEPSG(3665)
TRANS = osr.CoordinateTransformation(IN,OUT)

'''
Parameters:
    latitude, longitude: coordinates of a point in MRDS data
    length: the length of the square enclosing the point
    
    Returns minx, miny, maxx, and maxy coordinates of the square
'''
def vertices(latitude, longitude, length):
    # latitude to radians
    r_lat = latitude * pi / 180
    
    a = float(length) / (4 * R)
    diff_long = asin(sin(a) / cos(r_lat)) * 2 * 180 / pi
    diff_lat = a * 2 * 180 / pi
    
    
    projWin = TRANS.TransformPoint(longitude - diff_long, latitude + diff_lat)[:-1] + \
            TRANS.TransformPoint(longitude + diff_long, latitude - diff_lat)[:-1]
    
    return projWin
 

def pixel_centered_square(gt, lng, lat, D):
    forward_trans = Affine.from_gdal(*gt)
    reverse_trans = ~forward_trans
    px, py = reverse_trans * (lng, lat)
    px, py = int(px + 0.5), int(py + 0.5) # round to int pixel coordinate
    
    ulx, uly, lrx, lry = px - int(D/2), py - int(D/2), px + int(D/2), py + int(D/2)
    
    ulx, uly = forward_trans * (ulx, uly)
    lrx, lry = forward_trans * (lrx, lry)
    return (ulx, uly, lrx, lry)


'''
    Reads raster image files, crops rasters based on coordinates in MRDS and 
    stores the stored rasters into the database
'''
def get_raster_grids(rasters):
    # Connect to the PostgreSQL database server
    conn = None
    try:
        # Establishing database connection
        conn = psycopg2.connect(host = dbhost, database = dbname,
                            user = dbuser, password = dbpass)
        cur = conn.cursor()
        cur.execute('SELECT latitude, longitude, site_id FROM t_site;')
        mrds = cur.fetchall()
        
        if rasters is not None:
            files = rasters
        else:
            cur.execute('SELECT filename FROM t_raster_master')
            files = cur.fetchall()

        cur.execute(
            "prepare putrasters as "
            "insert into t_raster_cropped(raster_name,site_id,resolution,filename,filepath) values($1,$2,$3,$4,$5)")
	
        for D in GS:
            rsln = str(D) + 'x' + str(D)
            for fl in files:
                print('Processing ' + fl[0])
                fname = fl[0][:-4]
                dirname = cpdLoc + '/' + rsln + '/' + fname + '/'
                if not os.path.isdir(dirname):
                    os.makedirs(dirname)

                for site in mrds:
                    siteid = str(site[2])
                    imgname = fname + '_' + siteid + '.tif'
                    clipd = dirname + imgname
                    ds = gdal.Open(orgLoc + '/' + rsln + '/' + fl[0])
                    gt = ds.GetGeoTransform()
                    corners = pixel_centered_square(gt, site[1], site[0], D)
                    gdal.Translate(clipd, ds, projWin = corners)
                    cur.execute('execute putrasters (%s, %s, %s, %s, %s)', 
                        (fname, siteid, rsln, imgname, dirname))

        conn.commit()
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == '__main__':
    rasters = None
    if len(sys.argv) > 1:
        rasters = []
        for f in sys.argv[1:]:
            i = f.split('/')
            rasters.append(i[len(i) - 1])

    get_raster_grids(rasters)
