import pandas as pd
import json
from datetime import date

class Disk(object):
    
    def __init__(self, folder_name):
        self.filepath = r'./config.json'
        self.folder_name = folder_name
        with open(self.filepath, "r") as jsonFile:
            self.data = json.load(jsonFile)

    def _save_dataframe(self, file_str, df):

        date_str = date.today().strftime("%Y-%m-%d")
        filepath = f'./files/{self.folder_name}/{date_str}-{file_str}.csv'
        self.data['mock-db'][self.folder_name][file_str] = filepath
        df.to_csv(filepath, sep='\t', index=False)

        with open(self.filepath, "w") as jsonFile:
            json.dump(self.data, jsonFile)
            
    def save_participants(self, participants_df):
        self._save_dataframe('participants', participants_df)

    def save_responses(self, responses_df):
        responses_df = self._remove_new_lines(responses_df, 'TEXT')
        responses_df = self._remove_new_lines(responses_df, 'VALUE')
        self._save_dataframe('responses', responses_df)

    def save_wearbles(self, wearbles_df):
        self._save_dataframe('wearables', wearbles_df)
        
    def _remove_new_lines(self, df, column_name):
        df[column_name].replace('\\n',' ', regex=True, inplace=True)
        return df
        
    def read_by_label(self, label, sep='\t'):
        return pd.read_csv(self.data[self.folder_name][label], sep=sep)