import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import models, transforms
from sklearn.model_selection import train_test_split
from utils.manuscript_dataset import ManuscriptDataset

# Image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

dataset = ManuscriptDataset(csv_file='data/ground_truth_labels.csv', transform=transform)
train_data, valid_data = train_test_split(dataset, test_size=0.2, random_state=42)

train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
valid_loader = DataLoader(valid_data, batch_size=32, shuffle=False)

# Step 2: Model Architecture

model = models.resnet50(pretrained=True)
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, 1)

# Step 3: Training

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model.to(device)

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training loop
for epoch in range(10):  # example epochs
    model.train()
    running_loss = 0.0
    for i, data in enumerate(train_loader):
        inputs, labels = data['image'].to(device), data['skew_angle'].to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs.squeeze(), labels.float())
        loss.backward()
        optimizer.step()
        running_loss += loss.item()

    print(f"Epoch {epoch + 1}, Loss: {running_loss / len(train_loader)}")

# Step 4: Evaluation

model.eval()
error = 0.0
with torch.no_grad():
    for data in valid_loader:
        images, labels = data['image'].to(device), data['skew_angle'].to(device)
        outputs = model(images)
        error += ((outputs.squeeze() - labels.float()) ** 2).sum().item()

mse = error / len(valid_data)
print(f"Mean Squared Error on the validation set: {mse}")
