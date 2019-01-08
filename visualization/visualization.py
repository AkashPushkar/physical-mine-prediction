import pandas as pd
import numpy as np
from sklearn.datasets import fetch_mldata
import psycopg2
import matplotlib.image as mg 
import matplotlib.pyplot as plt
from pdb import set_trace as st
from scipy import misc

from PIL import Image
from osgeo import gdal 

import cv2

file1 = '/mnt/F2D85B4ED85B0FE9/Google Drive/My Data/kynes.ai/code/main/GeologicAgeLow_10139529.tif'
file2 = '/home/akash/ubuntu/kynesfield/datasets/clipped/64x64/AeroMag/AeroMag_203.tif'
# a1 = cv2.imread(file1, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
# a2 = misc.imread(file2)

# cv2.imshow(file)

ds1 = gdal.Open(file1)
ds2 = gdal.Open(file2)
a3 = np.array(ds1.ReadAsArray())
a4 = np.array(ds2.ReadAsArray())
# st()
# a = np.append(myarray1, myarray2, axis=2)

st()

# read images

# create_engine(dialect+driver://username:password@host:port/database)
# a = create_engine("postgresql+psycopg2://postgres:kynes@")

# [out] (70000, 784) (70000,)

# 

# data = np.random.rand(2,2,2)

# data1 = cv2.imread('image.jpeg')

# data1 = np.empty([1250,1250])

# # data2= cv2.imread('image.jpeg')
# data2 = np.empty([1250,1250, 1])
# data = np.concatenate((data1, data2) , axis =2)

# st()


# plt.imshow(data)
# plt.show()
# img = Image.fromarray(data, 'RGB')

# fig, a = plt.subplots(2,2,True)
# # st()
# # for i in a:
# 	# st()
# 	# i.imshow(img)

# a[0,0].imshow(img)
# a[0,1].imshow(img)
# a[1,0].imshow(img)
# a[1,1].imshow(img)

