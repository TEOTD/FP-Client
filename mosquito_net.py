import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
from io import BytesIO
import os

weightsPath = os.path.join('static', os.path.join('weights', 'model.pt'))

class MosquitoNet(nn.Module):
    
    def __init__(self):
        super(MosquitoNet, self).__init__()
        
        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        
        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        
        self.layer3 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
            
        self.fc1 = nn.Linear(64*15*15, 512)
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, 2)
        self.drop = nn.Dropout2d(0.2)
        
    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        out = out.view(out.size(0), -1)    # flatten out a input for Dense Layer
        out = self.fc1(out)
        out = F.relu(out)
        out = self.drop(out)
        out = self.fc2(out)
        out = F.relu(out)
        out = self.drop(out)
        out = self.fc3(out)
        
        return out 

def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize((120, 120)),
        transforms.ColorJitter(0.05),
        transforms.ToTensor(), 
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])
    image = Image.open(BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)   

def get_model():
    weights = torch.load(weightsPath, map_location=torch.device("cpu"))
    model = MosquitoNet()
    model.load_state_dict(weights)

    return model

def train_model(image, input_label):
    print(input_label)
    model = get_model()
    label = torch.tensor(input_label, dtype=torch.long)
    print(label)
    error = nn.CrossEntropyLoss()
    learning_rate = 0.001
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    model.train()

    tensor = transform_image(image_bytes=image)

    optimizer.zero_grad()
    logps = model.forward(tensor)
    loss = error(logps, label)
    loss.backward()
    optimizer.step()

    print("[Log] train loss", loss.item())

    torch.save(model.state_dict(), weightsPath)
    
    return loss.item()