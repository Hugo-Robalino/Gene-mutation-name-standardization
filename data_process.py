from datasets import DatasetDict, load_dataset
import json, random

random.seed(1492)

def load_dataset_subsets(raw_dataset):
    
    #read type of dataset
    with open(raw_dataset, 'r') as file:
        type = json.load(file)['type']
    
    #loading dataset
    if type == 'poc':
        raw_dataset = load_dataset('json', data_files=raw_dataset, field='data')['train']
        ds_train = raw_dataset.train_test_split(test_size=.3, seed=1492)
        ds_val_test = ds_train['test'].train_test_split(test_size=.5, seed=1492)
        data = DatasetDict({
                'train' : ds_train['train'],
                'val' : ds_val_test['train'],
                'test' : ds_val_test['test']
                })
    else:
        ds_train = load_dataset('json', data_files=raw_dataset, field='train')['train']
        ds_val = load_dataset('json', data_files=raw_dataset, field='val')['train']
        ds_test = load_dataset('json', data_files=raw_dataset, field='test')['train']
        data = DatasetDict({
                'train' : ds_train.shuffle(seed=1492),
                'val' : ds_val.shuffle(seed=1492),
                'test' : ds_test.shuffle(seed=1492)
                })
    
    return data