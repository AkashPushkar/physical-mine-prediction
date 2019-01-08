import input3
from torch.utils.data import Dataset, DataLoader
from sqlalchemy import create_engine
from pdb import set_trace as st
import os
import pandas as pd
from scipy import misc


conn = input3.connectToServer()

a = input3.data1(conn)

data = DataLoader(a, batch_size= 3)

for i_batch, sample_batched in enumerate(data):
	# st()
	print(i_batch)
	# st()
	print(sample_batched)
	st()
	# break