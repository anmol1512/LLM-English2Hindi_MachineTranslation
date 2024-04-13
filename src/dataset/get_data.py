from datasets import load_dataset
from config.config import CfgNode as CN
import torch
from torch.utils.data import Dataset

class EnglishHindiDataset(Dataset):

    @staticmethod
    def get_default_config():
        '''Default configuration of dataset'''
        config=CN()

        config.dataset = 'cfilt/iitb-english-hindi'
        config.total_size = 127085
        config.test_size = 0.2
        config.seed = 100
        config.device = 'auto'

        return config
    
    def __init__(self, config):

        # Load the dataset
        self.data = load_dataset(config.dataset, split='train')
        
        # Select a subset of the data
        self.data = self.data.select(range(config.total_size))
        
        # Split the data into train and test sets
        self.data = self.data.train_test_split(test_size = config.test_size, seed = config.seed)
        
        # Check if CUDA is available and set the device accordingly
        if config.device == 'auto':
            self.device=torch.device('cuda:0') if torch.cuda.is_available() else torch.device('cpu')
        else:
            self.device=torch.device(config.device)

    def __len__(self):
        # Optionally implement a way to return total size if needed, or raise NotImplementedError
        raise NotImplementedError("This doesn't support a single length. Use __len__(split) instead.")

    def __len__(self, split):
        # Return the number of items in a specific dataset split
        return len(self.data[split])

    def __getitem__(self, idx):
        if isinstance(idx, tuple):
            # Retrieve an item by index
            split, idx = idx
            item = self.data[split][idx]
            return {'english': item['translation']['en'], 'hindi': item['translation']['hi']}
        elif idx in ('train', 'test'):
            return self.data[idx]  
        else:
            raise ValueError("Must specify ('train', idx) or ('test', idx) to fetch data.")

