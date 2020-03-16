
from pathlib import Path

import torch
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from PIL import Image

class IrasutoyaDataset(Dataset):
    def __init__(self, image_size):
        self.image_paths = self._load()
        self.length = len(self.image_paths)
        self.transform = transforms.Compose([
            transforms.Resize(image_size),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
    
    def __len__(self):
        return self.length

    def __getitem__(self, index):
        image_path = self.image_paths[index]

        image = Image.open(image_path)
        image = self.transform(image)

        return image

    def _load(self):
        base = Path('/usr/src/data/images')
        paths = base.glob('*.jpg')
        paths = [str(path) for path in paths]

        return paths

def get_dataset(
    image_size,
    batch_size=32
):
    dataset = IrasutoyaDataset(image_size=image_size)
    dataset = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    return dataset

if __name__=='__main__':
    dataset = get_dataset(image_size=(64, 64), batch_size=32)
    for image in dataset:
        print(image.size())
        break
