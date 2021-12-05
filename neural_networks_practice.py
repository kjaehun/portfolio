## Neural Networks practice
## 11/04/2021

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms

## returns a dataloader for the training set or the test set
def get_data_loader(training = True):
    ## input preprocessing
    custom_transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])
    ## retrieve MNIST dataset (that is preprocessed)
    train_set = datasets.MNIST('./data', train=True, download=True,transform=custom_transform)
    test_set = datasets.MNIST('./data', train=False,transform=custom_transform)

    if training == True:
        loader = torch.utils.data.DataLoader(train_set, batch_size = 50)
    else:
        loader = torch.utils.data.DataLoader(test_set, batch_size = 50)
    return loader

def build_model():
    model = nn.Sequential(
        nn.Flatten(),           # convert 2D pixel array to 1D array
        nn.Linear(784, 128),    
        nn.ReLU(),              # dense layer with 128 nodes and a ReLU activation
        nn.Linear(128, 64),
        nn.ReLU(),              # dense layer with 64 nodes and a ReLU activation
        nn.Linear(64, 10)       # dense layer with 10 nodes
        )
    return model


def train_model(model, train_loader, criterion, T):
    # use SGD with a learning rate of 0.001 and momentum of 0.9
    opt = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    model.train()

    for epoch in range(T):
        running_loss = 0.0
        correct = 0
        total = 0
        for i, data in enumerate(train_loader, 0):
            inputs, labels = data
            opt.zero_grad()
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            loss = criterion(outputs, labels)
            loss.backward()
            opt.step()

            running_loss += loss.item()
        # print out accuracy and loss for each epoch
        print("​Train Epoch: {:d}   Accuracy: {:5d}/60000({:.2f}%)   Loss: {:.3f}".
              format(epoch, correct, (100 * correct / total), running_loss / i))
        
def evaluate_model(model, test_loader, criterion, show_loss = True):
    model.eval()

    correct = 0
    total = 0
    running_loss = 0.0
    with torch.no_grad():
        for data in test_loader:
            images, labels = data
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            loss = criterion(outputs, labels)
            running_loss += loss.item()
    # print out accuracy, and print out average loss if specified
    if show_loss == True:
        print("Average loss: {:.4f}".format(running_loss / total))
    print("Accuracy: {:.2f}%".format(100 * correct / total))
        
## predict labels of a select few images
def predict_label(model, test_images, index):
    # test_images should be a torch tensor with the shape nx1x28x28 where n is the number of images
    N = len(test_images[index])
    logits = model(test_images[index])
    class_names = ['zero', 'one', 'two', 'three',
                   'four', 'five', 'six', 'seven', 'eight', 'nine']
    # use Softmax to convert output of final dense layer into probabilities
    prob = F.softmax(logits, dim = N)
    prob = torch.reshape(prob, [-1])
    b1 = torch.argmax(prob)
    prob2 = torch.cat([prob[0:b1], prob[b1+1:]])
    b2 = torch.argmax(prob2)
    prob3 = torch.cat([prob2[0:b2], prob2[b2+1:]])
    b3 = torch.argmax(prob3)
    b2t = b2
    if b1 <= b2:
        b2t += 1
    if b1 <= b3:
        b3 += 1
    if b2 <= b3:
        b3 += 1
    b2 = b2t
    a1 = b1.item()
    a2 = b2.item()
    a3 = b3.item()
    print("{}: {:.2f}%".format(class_names[a1], prob[a1].item() * 100))
    print("{}: {:.2f}%".format(class_names[a2], prob[a2].item() * 100))
    print("{}: {:.2f}%".format(class_names[a3], prob[a3].item() * 100))
