import torch
import torch.nn as nn
import torch.nn.functional as F 
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, WeightedRandomSampler
import torch.cuda

import numpy as np 
import pandas as pd

from sqlalchemy import create_engine
from pdb import set_trace as st
import os

# from ../../utils import input3
import datasetCustomClass
import data_augmentation as da

'''
Initialization 
'''

device = torch.device('cuda')
numberEpoch = 2
batchSize = 50
trainError = []
testError = []
batchNumber = []


'''
Reading the data
'''

#samplingMethod = WeightedRandomSampler([0.05,0.95],25232,True)
#st()
conn = datasetCustomClass.connectToServer()
a = datasetCustomClass.data1(conn)
traindataloader = DataLoader(a, batch_size = batchSize)
#traindataloader = DataLoader(a, batch_size = batchSize,sampler=samplingMethod)


'''
Defining architecture
'''
class Net(nn.Module):
	def __init__(self):
		super(Net, self).__init__()

		self.conv1 = nn.Conv2d(23, 48, 5)
		self.conv2 = nn.Conv2d(48, 96, 5)

		self.fc1 = nn.Linear(13*13*96, 1600)
		self.fc2 = nn.Linear(1600, 400)
		self.fc3 = nn.Linear(400, 2)
		#self.lastLayer = nn.Sigmoid()

	def forward(self, x):
		#st()
		x = F.max_pool2d(F.relu(self.conv1(x)),(2,2))
		#st()
		x = F.max_pool2d(F.relu(self.conv2(x)),(2,2))
		#st()
		x = x.view(-1, self.num_flat_features(x))
		#st()
		x = F.relu(self.fc1(x))
		#st()
		x = F.relu(self.fc2(x))
		x = F.relu(self.fc3(x))
		#st()
		#x = self.lastLayer(x)
		#st()
		return x

	def num_flat_features(self, x):
		size = x.size()[1:]
		num_features = 1
		for s in size:
			num_features *= s
		return num_features

net = Net()

print (net)
# Putting the model on device: CUDA
net.to(device)


# params = list(net.parameters())
# print(len(params))
# for i in params:
# 	print(i.size())


'''
Defining the loss function and optimizer
'''

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.00001, momentum = 0.9)


'''
training of the network
'''


for epoch in range(numberEpoch):

	running_loss = 0
	for i_batch, batch_sampled in enumerate(traindataloader):
		# inputs
		inputs = batch_sampled['input'].float()
		#st()
		inputs = da.normalizeInput(inputs)
		#st()
		# Putting input on GPU
		inputs = inputs.to(device)
		#st()
		label = batch_sampled['class']
		label = label.to(device)
		
		# parameters
		optimizer.zero_grad()
		#st()
		# forward + backward + optimize
		#st()
		out = net(inputs)
		loss = criterion(out, label)
		
		loss.backward()
		optimizer.step()
		#st()
		print("Epoch:{},Batch:{},positive classes:{}.loss{}".format(epoch, i_batch,label.sum(),loss.item()))
		

		# printing stat
		running_loss += loss.item()
		if i_batch % 200 == 0:
			trainError.append(running_loss/200)
			batchNumber.append(i_batch+1)
			print("This result is at the interval of 200 Epochs: Epoch:{},Batch:{},loss:{}".format(epoch, i_batch, loss.item()))
			running_loss = 0

print('Training Finished')

