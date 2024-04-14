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
    cfilt = EnglishHindiDataset(config.data)
    
   
    '''Data Preprocessing'''
    print('DATA IS COOKING..................')
    # opus-mt
    opus_processor = DataProcessor('opus-mt-en-hi')
    opus_tokenized_data = opus_processor.prepare_dataset(cfilt.data)


    # m2m100
    m2m100_processor = DataProcessor('m2m100')
    m2m100_tokenized_data = m2m100_processor.prepare_dataset(cfilt.data)

    # mbart-large-50
    mbart_processor = DataProcessor('mbart-large-50')
    mbart_tokenized_data = mbart_processor.prepare_dataset(cfilt.data)

    # madlad-400
    madlad_processor = DataProcessor('madlad-400')
    madlad_tokenized_data = madlad_processor.prepare_dataset(cfilt.data)