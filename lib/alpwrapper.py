import json
import os
import pandas as pd
from IPython.utils import io

from contextlib import redirect_stdout
from lib.schema import SchemaManager
import io

class QueryWrapper(object):
    
    def __init__(self, schema):
        self.settings = SchemaManager.get_settings(schema)
        self.schema = schema
    
    @staticmethod
    def _import_alp_libs():
        from pyqe import Query, Result, Person, Interactions
        
    def get_participants(self):
        query = self.prepare_query('Participants')
        df = self.execute(query, [Person.Patient()]) 
        return self.procesing_participants_table(df)

    def procesing_participants_table(self, df):
        df = df.rename(columns={
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
    
    def get_wearables(self):
        query = self.prepare_query('Wearables')
        d = query.get_entities_dataframe_cohort([
            'patient.interactions.observation.attributes.obsid',
            'patient.interactions.observation.attributes.obsdate',
            'patient.interactions.observation.attributes.pid', 
            'patient.interactions.observation.attributes.obsconceptcode',
            'patient.interactions.observation.attributes.obsname',
            'patient.interactions.observation.attributes.numval',
            'patient.interactions.observation.attributes.unit',
        ])
        r = Result().download_all_entities_dataframe(d)
        return self.procesing_wearables_table(r['observation'])

    def procesing_wearables_table(self, df):
        df = df.rename(columns={
            'obsid': 'WEARABLE_ID',
            'obsdate': 'AUTHORED',
            'pid': 'ALP_ID',
            'obsconceptcode': 'WEARABLE_TYPE',
            'obsname': 'WEARABLE_NAME',
            'numval': 'VALUE',
            'unit': 'UNIT'
        })
        column_names = ['WEARABLE_ID', 'AUTHORED', 'ALP_ID', 'WEARABLE_TYPE', 'WEARABLE_NAME', 'VALUE', 'UNIT']
        df = df[column_names] if df.shape[0] else pd.DataFrame(columns = column_names)
        return df
        
    def get_responses(self):
        query = self.prepare_query('Responses')
        df = self.execute(query, [Interactions.Questionnaire("q")])
        return self.procesing_responses_table(df)
    
    def procesing_responses_table(self, df):    
        df = df.rename(columns={
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
            'valuetype': 'VALUE_TYPE'
        })
        column_names = ['ALP_ID', 'VERSION', 'AUTHORED', 
                        'QUESTIONNAIRE', 'LINK_ID', 'VALUE', 
                        'VALUECODING_CODE', 'LANGUAGE', 'TEXT', 'QUESTIONNAIRE_ID']
        df = df[column_names] if df.shape[0] else pd.DataFrame(columns = column_names)
        df['AUTHORED'] = pd.to_datetime(df['AUTHORED'])
        temp = df['QUESTIONNAIRE'].str.split('/', expand=True)
        df['QUESTIONNAIRE'] = temp[len(temp.columns) - 1]
        return df
        
    def prepare_query(self, cohort_name):
        QueryWrapper._import_alp_libs()
        q = Query(cohort_name=cohort_name) 
        study_id = study_settings.get_study()
        config_id = study_settings.get_config()
        q.set_study(study_id)
        q.set_study_config(config_id)
        return q
    
    def execute(self, query, filters):
        query.add_filters(filters);
        f = io.StringIO()
        with redirect_stdout(f):
            request = query.get_dataframe_cohort(); # printing to screen
            df = Result().download_dataframe(request)
        return df
    
    def print_all_wearble_attirbutes(self):
        query = self.prepare_query('Create query to make this work')
        entityName = 'observation'
        PAConfig()._get_frontend_config(
            os.environ['PYQE_STUDY_CONFIG_ID'], 
            os.environ['PYQE_STUDY_CONFIG_VERSION'])['config']['patient']['interactions'][entityName]['attributes'].keys()

