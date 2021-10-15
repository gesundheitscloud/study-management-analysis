import json
import os
import pandas as pd
from pyqe import Query, Result, Person, Interactions
from IPython.utils import io
from enum import Enum

from contextlib import redirect_stdout
import io
    
# (1) Accept - fb4269d3-f6ac-4f81-85da-b80ce277793e
# (2) CRONOS by DGPM - 38ce29c0-eb76-45cc-ba4f-56395f8c49e0
# (3) CoCoMo  - e14cc34d-b78e-46ad-a7c6-f6159f1f1c96
# (4) D4L patients registry - 3ce0e946-2aff-4960-aaca-d7fa43bdcc8e
# (5) ECOV - f875fdc4-c180-45f3-bdbb-a68fb1476338
# (6) RKI panel - 0e858bc9-3be8-4d44-9139-97e6e678a334

class Schema(Enum):
    ACCEPT = 1
    CRONOS = 2
    COCOMO = 3
    WAITING_LIST = 4
    ECOV = 5
    RKI_PANEL = 6

class Settings():
    def __init__(self, study_id, has_config=False):
        self.study_id = study_id
        self.has_config = has_config
    def get_study(self):
        return self.study_id
    def get_config(self):
        DEFAULT_CONFIG = 'daac6e40-9fdc-48f8-bd9b-181571102d91'
        return DEFAULT_CONFIG if self.has_config else None

class Database(object):
    
    def __init__(self, schema):
        all_settings = {}
        all_settings[Schema.ACCEPT] = Settings('fb4269d3-f6ac-4f81-85da-b80ce277793e', True)
        all_settings[Schema.CRONOS] = Settings('38ce29c0-eb76-45cc-ba4f-56395f8c49e0', True)
        all_settings[Schema.COCOMO] = Settings('e14cc34d-b78e-46ad-a7c6-f6159f1f1c96', False)
        all_settings[Schema.WAITING_LIST] = Settings('3ce0e946-2aff-4960-aaca-d7fa43bdcc8e', True)
        all_settings[Schema.ECOV] = Settings('f875fdc4-c180-45f3-bdbb-a68fb1476338', True)
        all_settings[Schema.RKI_PANEL] = Settings('0e858bc9-3be8-4d44-9139-97e6e678a334', True)
        study_settings = all_settings[schema]
        self.study_id = study_settings.get_study()
        self.config_id = study_settings.get_config()
        self.schema = schema
        
    def get_participants(self):
        query = self.prepare_query('Participants')
        df = self.execute(query, [Person.Patient()], {
            'pid': 'ALP_ID',
            'alpid': 'HUH?',
            'status': 'STATUS',
            'externalid': 'EXTERNAL_ID',
            'periodstart': 'START_DATE',
            'periodend': 'END_DATE',
        })
        column_names = ['ALP_ID', 'EXTERNAL_ID', 'STATUS', 'START_DATE', 'END_DATE']
        # if df is empty alp returns empty df without columns
        df = df[column_names] if df.shape[0] else pd.DataFrame(columns = column_names)
        return df
        
    def get_responses(self):
        query = self.prepare_query('Responses')
        df = self.execute(query, [Interactions.Questionnaire("q")], {
            'pid': 'ALP_ID',
            'questionnaireversion': 'VERSION',
            'questionnaireauthored': 'AUTHORED',
            'questionnairereference' : 'QUESTIONNAIRE',
            'linkid': 'LINK_ID',
            'questionnaireid': 'QUESTIONNAIRE_ID',
            'questionnairelanguage': 'LANGUAGE',
            'text': 'TEXT',
            'value': 'VALUE',
            'valuecodingvalue': 'VALUECODING_CODE',
            'valuetype': 'VALUE_TYPE',
            '_interaction_id': 'INTERACTION_ID'
        })
        column_names = ['ALP_ID', 'VERSION', 'AUTHORED', 
                   'QUESTIONNAIRE', 'LINK_ID', 'VALUE', 
                   'VALUECODING_CODE', 'LANGUAGE', 'TEXT', 'INTERACTION_ID']
        df = df[column_names] if df.shape[0] else pd.DataFrame(columns = column_names)
        df['AUTHORED'] = pd.to_datetime(df['AUTHORED'])
        if df.shape[0]:
            temp = df['QUESTIONNAIRE'].str.split('/', expand=True)
            df['QUESTIONNAIRE'] = temp[len(temp.columns) - 1]
        return df
    
    def prepare_query(self, cohort_name):
        q = Query(cohort_name=cohort_name)        
        q.set_study(self.study_id)
        if self.config_id:
            q.set_study_config(self.config_id)
#         q.get_study_list()
#         q.get_config_list()
        return q
    
    def execute(self, query, filters, columns_map):
        query.add_filters(filters);
        f = io.StringIO()
        with redirect_stdout(f):
            request = query.get_dataframe_cohort(); # printing to screen
            df = Result().download_dataframe(request).rename(columns=columns_map)
        return df