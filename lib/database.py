import pandas as pd
import json

from lib.schema import Schema
from lib.alpwrapper import QueryWrapper
from lib.mock_db import MockDatabase


class Database(object):
    
    @staticmethod
    def check_pandas_version():
    # Check that pandas version is 1.3.1 and above.
    # Reason: the column AUTHORED has mix values of YYYY-MM-DD and YYYY-MM-DD HH:MM:SS
    # pd.to_datetime for versions below 1.3.1 return NaT for YYYY-MM-DD
        ver = [int(i) for i in pd.__version__.split('.')]
        if (ver[0] >= 1) & (ver[1] >= 3) & (ver[2]>= 1) is False:
            raise Exception('Update your pandas version to 1.3.1 and above')
    
    def __init__(self, schema, is_mock=None):
        Database.check_pandas_version()
        self.schema = schema
        with open(r'./config.json', "r") as jsonFile:
            data_lib = json.load(jsonFile)
        if is_mock is None:
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