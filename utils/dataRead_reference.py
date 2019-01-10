'''
For getting the data from the database on AWS instance, using the datasetCustomClass.py

'''
from torch.utils.data import Dataset, DataLoader
from sqlalchemy import create_engine
from pdb import set_trace as st
import os
import pandas as pd
import numpy as np
import datasetCustomClass

'''
Add the next 3 lines in your model file for reading the data. Please place the datasetCustomClass.py in the same folder as the 
model file you are running
'''

conn = datasetCustomClass.connectToServer()

'''
Please set the value of set in the below to: 'Train', 'Test' or 'Validate' depending on from which set the data needs to be iterated
using the respective dataloader created. By default it is set to 'Train'
'''

a = datasetCustomClass.data1(connection = conn, set = 'Train')

dataloader = DataLoader(a, batch_size = 50)


'''
Example of getting data from the iterator created above 
'''

for i_batch, sample_batched in enumerate(dataloader):
	# st()
	print(i_batch)
	# st()
	#print(sample_batched)
	print(np.shape(sample_batched['input']))
	if i_batch == 4:
		break