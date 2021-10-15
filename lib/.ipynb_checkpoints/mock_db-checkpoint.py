import pandas as pd
import json

class Database(object):
    
    def __init__(self, base_path, folder_name):
        with open(base_path + '/config.json', 'r') as f:
            files = json.load(f)
        self.data_lib = files[folder_name]
                
    def _to_date(self, df, col_name):
        return pd.to_datetime(df[col_name].str.split(' ').str[0], 
                              format='%Y-%m-%d', errors='coerce')    
    
    def get_participants(self):
        if self.data_lib['alp']:
            df = pd.read_csv(data_lib['participants'], sep='|')
            df.columns = df.columns.str.strip()
            df = df[['ALP_ID', 'STATUS', 'PERIOD_START']]
            df = df.drop(labels=0, axis=0)
        else:
            df = pd.read_csv(self.data_lib['participants'], sep='\t')
            df.drop(columns=['Unnamed: 0'], inplace=True)

        df['START_DATE'] = self._to_date(df, 'START_DATE')
        df['END_DATE'] = self._to_date(df, 'END_DATE')
        return df
        
    def get_responses(self):
        if self.data_lib['alp']:
            raise Exception('Not implmented yet.')
        else:
            df = pd.read_csv(self.data_lib['responses'], sep='\t')
        
        df['AUTHORED'] = self._to_date(df, 'AUTHORED')
        return df
    
    def _remove_new_lines(self, df, column_name):
        df[column_name].replace('\\n',' ', regex=True, inplace=True)
        
    def save_to_csv(self, participants_df, responses_df):
        participants_df.to_csv(self.data_lib['participants'], sep='\t')
        self._remove_new_lines(responses_df, 'TEXT')
        self._remove_new_lines(responses_df, 'VALUE')
        responses_df.to_csv(self.data_lib['responses'], sep='\t')