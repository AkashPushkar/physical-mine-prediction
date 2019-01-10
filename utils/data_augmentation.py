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


def augmentInput(connection, over_sampling= 1, flip= 1, rotate=1):

	successID = connection.execute("SELECT site_id FROM t_site WHERE classifier != 'E' AND model_category = 'Train' AND classifier = 'S'")
	successID = successID.fetchall()
	successID = np.asarray(successID)
	
	ao = overSampling(successID ,over_sampling)
	af = flipID(successID ,flip)
	ar = rotateID(successID ,rotate)
	#st()
	successID = np.concatenate((np.transpose(successID), [ao], [af], [ar]), axis = 1)
	#st()
	return successID

def overSampling(successID, n):
	sum = []
	for i in range(n):
		sum = np.append(sum, successID)
	return sum

def flipID(successID, n):
	sum = [0]
	for i in range(n):
		sum1 = np.transpose(np.concatenate((successID + 0.01, successID + 0.02, successID+0.03), axis=0))
		#st()	
		sum = np.append(sum, sum1)
	return sum[1:]

def rotateID(successID, n):
	sum = [0]
	for i in range(n):
		sum1 = np.transpose(np.concatenate(((successID + 0.11), (successID + 0.12), (successID+0.13)), axis =0))
		sum = np.append(sum, sum1)
	return sum[1:]	

def flip(image, flipType):
	
	if flipType == 0.01:
		for i in range(np.shape(image)[0]):
			image[i,:,:] = np.flipud(image[i,:,:])	
	elif flipType == 0.02:
		for i in range(np.shape(image)[0]):
			image[i,:,:] = np.fliplr(image[i,:,:])
	else:
		for i in range(np.shape(image)[0]):
			image[i,:,:] = np.flipud(image[i,:,:])
			image[i,:,:] = np.fliplr(image[i,:,:])

	return image


def rotate(image, flipType):
	if flipType == 0.11:
		np.rot90(image, k=1, axes=(1,2))
	elif flipType == 0.12:
		np.rot90(image, k=2, axes=(1,2))
	else:
		np.rot90(image, k=-1, axes=(1,2))

	return image
