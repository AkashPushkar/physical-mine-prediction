import numpy as np
import pandas as pd
from pdb import set_trace as st

def normalizeInput(x):
		for batch in range(np.shape(x)[0]):
				for channel in range(np.shape(x)[1]):

						# Normalize from [0, 1] 
						minimum = x[batch, channel, :, :].min()
						maximum = x[batch, channel, :, :].max()
						if (maximum - minimum) == 0:
							maximum = maximum + 1                        	
						x[batch,channel,:,:] = (x[batch,channel,:,:] - minimum) * 255 / (maximum - minimum)


						# m = x[batch, channel, :, :].mean()
						# stdev = x[batch, channel, :, :].std()
						# x[batch,channel,:,:] = (x[batch,channel,:,:] - m) / stdev
						# x[batch,channel,:,:] = x[batch,channel,:,:] - m
		return x

def dataAugmentation(**kwargs):
	successID = con.execute("SELECT site_id FROM t_site WHERE classifier != 'E' AND model_category = 'Train' AND classifier = 'S'")
	successID = successID.fetchall()




def overSampling(con):
	sum = []
	for i in range(4):
		sum = sum + successID
	return successID

def flip():


def rotate():


