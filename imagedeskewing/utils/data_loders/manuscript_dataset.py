from torch.utils.data import DataLoader, Dataset
import pandas as pd
from PIL import Image


class ManuscriptDataset(Dataset):
    def __init__(self, csv_file, transform=None):
        self.data = pd.read_csv(csv_file)
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_name = self.data.iloc[idx, 1]
        image = Image.open(img_name)
        skew_angle = self.data.iloc[idx, 2]
        sample = {'image': image, 'skew_angle': skew_angle}

        if self.transform:
            sample['image'] = self.transform(sample['image'])

        return sample
