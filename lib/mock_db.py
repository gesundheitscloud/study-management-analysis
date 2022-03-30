import pandas as pd
import json

from lib.schema import Schema

class Database(object):
    
    def __init__(self, schema):
        self.schema = schema
        filepath = r'./config.json'
        with open(filepath, 'r') as f:
            files = json.load(f)
        self.data_lib = files['mock-db']
        
    def get_participants(self):
        df = self._read_by_label('participants')
        df['START_DATE'] = pd.to_datetime(df['START_DATE'])
        df['END_DATE'] = pd.to_datetime(df['END_DATE'])
        return df

    def get_wearables(self):
        return self._read_by_label('wearables')
        
    def get_responses(self):
        df = self._read_by_label('responses')
        df['AUTHORED'] = pd.to_datetime(df['AUTHORED'])
        return df
        
    def _read_by_label(self, label, sep='\t'):
        files_obj = self.data_lib[self.schema.name]
        return pd.read_csv(files_obj[label], sep=sep)