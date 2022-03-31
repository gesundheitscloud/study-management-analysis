import pandas as pd
import json

from lib.schema import Schema
from lib.alpwrapper import QueryWrapper
from lib.mock_db import MockDatabase

class Database(object):
    
    def __init__(self, schema):
        self.schema = schema
        with open(r'./config.json', "r") as jsonFile:
            data_lib = json.load(jsonFile)
        is_mock = (data_lib['env'] == 'local_env')
        self.db = MockDatabase(schema) \
            if is_mock \
            else QueryWrapper(schema)

    def get_participants(self):
        df = self.db.get_participants()
        df['START_DATE'] = pd.to_datetime(df['START_DATE'])
        df['END_DATE'] = pd.to_datetime(df['END_DATE'])
        return df

    def get_wearables(self):
        return self.db.get_wearables()
        
    def get_responses(self):
        df = self.db.get_responses()
        df['AUTHORED'] = pd.to_datetime(df['AUTHORED'])
        return df