# -*- coding: utf-8 -*-
"""cnn1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12BWHToYZ-k7BplnIGub1lwmT5ci-AWAz
"""

import torch
from torch.utils.data import Dataset,DataLoader
import matplotlib.pyplot as plt
import torchvision

#loadinf data set
training_data = torchvision.datasets.CIFAR10(root='./data',train=True,download=True)

test_data = torchvision.datasets.CIFAR10(root='./data',train=False,download=True)

image, label = training_data[1]
plt.imshow(image)
print('Label:', label)

from torchvision.transforms import ToTensor

training_data = torchvision.datasets.CIFAR10(root='./data',train=True,transform=ToTensor())

test_data = torchvision.datasets.CIFAR10(root='./data',train=False,transform=ToTensor())

#creating data loader , we create them to use batch image and not give picture one by one to compiler so our run would become so much faster

train_loader = DataLoader(training_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64, shuffle=True)

for images, labels in train_loader:
    print(labels.shape)
    print(images.shape)
    break

#creating model

import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
       super().__init__()
       self.conv1 = nn.Conv2d(3,6,5)  #3=input channels, 6=output channel, 5=filter size(5*5)
       self.pool = nn.MaxPool2d(2,2)  #2=kernelsize, 2=stridesize
       self.conv2 = nn.Conv2d(6,16,5)
       self.fc1 = nn.Linear(16*5*5,120)  #fully connected layers, 16*5*5=features(filters*dimension of them) , outputfeatures=120
       self.fc2= nn.Linear(120,84)
       self.fc3= nn.Linear(84,10) # 10 = classes that we have(in classification)
    def forward(self,x):
       x = self.pool(F.relu(self.conv1(x)))
       x = self.pool(F.relu(self.conv2(x)))
       x = torch.flatten(x,1) #flatten all dimension except batch
       x = F.relu(self.fc1(x))
       x = F.relu(self.fc2(x))
       x = self.fc3(x)
       return x
net = Net()
print(net)

import torch.optim as optim
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(),lr=0.001, momentum=0.9)

for epoch in range(10):    #loop over the dataset multiple time
        running_loss=0.0
        for i, data in enumerate(train_loader, 0):
          #get the inputs; data is a list of[inputs, labels]
          inputs, labels = data

          #zero the parameter gradient
          optimizer.zero_grad()

          #forward + backward + optimize
          outputs = net(inputs)
          loss = criterion(outputs, labels)
          loss.backward()
          optimizer.step()

          #print statistics
          running_loss +=loss.item()
        print("loss:",running_loss)
print('finishes training')

correct = 0
total = 0
# since we are not training, we do not need to calculate the gradient for our output
with torch.no_grad():
   for data in test_loader:
     images, labels = data
     #calculate outputs by running images through the network
     outputs = net(images)
     #the class with the highest energy is what we choose as prediction
     _,predicted= torch.max(outputs.data, 1)
     total += labels.size(0)
     correct += (predicted == labels).sum().item()
   print(f'Acuure=acy of the network on the 10000 test image: {100 * correct//total}%')

#saving a model
torch.save(net.state_dict(), 'model.pth')
print('saved pytorch model .pth')