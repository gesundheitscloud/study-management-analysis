import pandas as pd
import json

from lib.schema import Schema
    
class MockDatabase(object):
    
    def __init__(self, schema, drop_index=True):
        self.schema = schema
        self.drop_index = drop_index
        env_name = 'local_env'
        with open(r'./config.json', "r") as jsonFile:
            data_lib = json.load(jsonFile)
        self.files = data_lib[env_name][self.schema.name]
        
    def get_participants(self):
        return self._read_file('participants')

    def get_wearables(self):
        return self._read_file('wearables')
        
    def get_responses(self):
        return self._read_file('responses') 
        
    def _read_file(self, file_label, sep='\t'):
        df = pd.read_csv(self.files[file_label], sep=sep, low_memory=False)
        return df.drop(columns=['Unnamed: 0'])