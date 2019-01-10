import numpy as np
import pandas as pd

def normalizeInput(x):
	for batch in range(np.shape(x)[0]):
		for channel in range(np.shape(x)[1]):
			minimum = x[batch, channel, :, :].min()
			maximum = x[batch, channel, :, :].max()
			x[batch,channel,:,:] = (x[batch,channel,:,:] - minimum) * 255 / (maximum - minimum)
	return x

def dataAugmentation(**kwargs):
	return 1 