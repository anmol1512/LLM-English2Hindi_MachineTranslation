from config.config import CfgNode as CN
from src.dataset.get_data import EnglishHindiDataset
from src.dataset.data_process import DataProcessor
import sys

# Getting all config
def get_config():
    config = CN()

    # SYSTEM CONFIG
    config.system = CN()
   
    #DATA CONFIG
    config.data = EnglishHindiDataset.get_default_config()

    return config

if __name__ == '__main__':

    'Get user configurations'
    config = get_config()
    user_config = sys.argv[1:]
    config.update_args(user_config)

    ''' Data Loading'''
    print('LOADING DATA.........................')
    data = EnglishHindiDataset(config.data)
    
    model_type = 'facebook/m2m100_418M'
    source_lang = "en"
    target_lang = "hi"
    
    # Initialize the data processor
    processor = DataProcessor(model_type, source_lang, target_lang)
    tokenized_data = processor.prepare_dataset(data)

