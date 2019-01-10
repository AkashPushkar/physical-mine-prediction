'''
This is custom class for reading the data from (PostgreSQl database + AWS local storage). 

This is to called from the model file. Please refer 'dataRead_reference.py' to see the example how to use this file 

'''

from torch.utils.data import Dataset, DataLoader
from sqlalchemy import create_engine
from pdb import set_trace as st
import os
import numpy as np
import gdal
import data_augmentation

def connectToServer():
	engine = create_engine('postgresql+psycopg2://postgres:kynes@54.185.63.248:5432/postgres')
	connection = engine.connect()
	return connection

# def increaseDataTemp(con):
# 	successID = con.execute("SELECT site_id FROM t_site WHERE classifier != 'E' AND model_category = 'Train' AND classifier = 'S'")
# 	successID = successID.fetchall()
# 	for i in range(4):
# 		successID = successID + successID

# 	return successID


class data1(Dataset):
	def __init__(self, connection, set='Train'):
		self.connection = connection

		a = (self.connection).execute("SELECT site_id FROM t_site WHERE classifier != 'E' AND model_category = '{}'".format(set))
		self.IDs = a.fetchall()

		# For increasing the data : Start
		if set = 'Train':
			successID = increaseDataTemp(self.connection)
			self.IDs = np.append(self.IDs, successID)

		# For increasing the data : End

		np.random.shuffle(self.IDs)


	def __len__(self):
		# l = (self.connection).execute("SELECT count(*) FROM t_site WHERE classifier != 'E' AND model_category = 'Train'")
		# l = l.fetchall()
		# # st()
		# return (l[0]['count'])

		return (len(self.IDs))

	def __getitem__(self, idx):
		
		siteID = self.IDs[idx]
		# siteID = 203
		a = (self.connection).execute("SELECT r.filename, r.filepath, s.classifier FROM t_site s, t_raster_cropped r WHERE r.site_id = {} AND s.site_id = r.site_id ".format(siteID[0]))
		a = a.fetchall()
		
		inputshapeX = 64
		inputshapeY = 64
		finalinput = np.zeros([1, inputshapeX, inputshapeY])
		finalpath = []
		label = a[0]['classifier']
		if label == 'F':
			label = 0
		else:
			label = 1

		for i in range(len(a)):
			
			path = os.path.join(a[i]['filepath'], a[i]['filename'])
			#path = path.replace('ubuntu','akash/ubuntu' )
			
			# read file from the local 
			img = gdal.Open(path)
			img = np.array(img.ReadAsArray())
			img = np.reshape(img, [-1, inputshapeX, inputshapeY])
			#img = misc.imread(path)

				
			finalinput = np.append(finalinput, img, axis=0)
			#st()

			# if i ==0:
			# 	break
			
		finalinput = np.delete(finalinput, 0, 0)
		sample = {'input':finalinput, 'class':label}
		
		return sample
