from torch.utils.data import Dataset, DataLoader
from sqlalchemy import create_engine
from pdb import set_trace as st
import os
import numpy as np
import cv2
from scipy import misc
import gdal

def connectToServer():
	engine = create_engine('postgresql+psycopg2://postgres:kynes@54.185.63.248:5432/postgres')
	connection = engine.connect()
	return connection


class data1(Dataset):
	def __init__(self, connection):
		self.connection = connection

		a = (self.connection).execute("SELECT site_id FROM t_site")
		self.IDs = a.fetchall()

	def __len__(self):
		l = (self.connection).execute("SELECT count(*) FROM t_site")
		l = l.fetchall()
		# st()
		return (l[0]['count'])

	def __getitem__(self, idx):
		
		siteID = self.IDs[idx]
		# siteID = 203

		a = (self.connection).execute("SELECT r.filename, r.filepath, s.classifier FROM t_site s, t_raster_cropped r WHERE r.site_id = %s AND s.site_id = r.site_id ", (siteID))
		a = a.fetchall()
		
		inputshapeX = 64
		inputshapeY = 64
		finalinput = np.zeros([1, inputshapeX, inputshapeY])
		finalpath = []
		label = a[0]['classifier']

		for i in range(len(a)):
			
			path = os.path.join(a[i]['filepath'], a[i]['filename'])
			#path = path.replace('ubuntu','akash/ubuntu' )
			
			# read file from the local 
			img = gdal.Open(path)
			img = np.array(img.ReadAsArray())
			img = np.reshape(img, [-1, inputshapeX, inputshapeY])
			#img = misc.imread(path)

			# finalpath = np.append(finalpath, path, axis=0)
				
			finalinput = np.append(finalinput, img, axis=0)
			#st()

			# if i ==0:
			# 	break
			
		finalinput = np.delete(finalinput, 0, 0)
		sample = {'input':finalinput, 'class':label}
		
		return sample
