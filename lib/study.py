from enum import Enum
import pandas as pd

class Study():
    def name(self):
        pass
    def demographic(self):
        pass
    def questionnaires(self):
        pass


class PanelStudy(Study):    
    
    def name(self):
        return "RKI-Panel"
    
    def demographic(self):
        return self.questionnaires()['Q1']
    
    def questionnaires(self):
        return {
            'Q1': 'S1', 
        }
    
class CronosStudy(Study):    
    
    def name(self):
        return "CRONOS+"
    
    def demographic(self):
        return self.questionnaires()['Q1']
    
    def questionnaires(self):
        return {
            'Q1': 'Q1_personal_info', 
            'Q2a': 'Q2a_coronoa_effects_pregnancy',
            'Q2b': 'Q2b_coronoa_effects_birth',
            'Q3': 'Q3_mood_in_pregnancy',
            'Q3a': 'Q3a_time_around_calc_delivery',
            'Q3b': 'Q3b_mood_after_delivery',
            'Q6': 'Q6_handling_challenges',
            'Q5' : 'Q5_final_questionnaire'
        }

class EcovStudy(Study):    
    
    def name(self):
        return "eCOV"
    
    def demographic(self):
        return self.questionnaires()['Q1']
    
    def questionnaires(self, acrnm=None):            
        all = {
            'Q1' : 'personal_info',
            'Q2' : 'corona_testing_and_symptoms',
            'Q3' : 'covid_exposition',
            'Q4a' : 'covid_first_vaccine',
            'Q4b' : 'covid_second_vaccine',
            'Q5a' : 'vaccination_side_effects_a',
            'Q5b' : 'vaccination_side_effects_b',
            'Q6' : 'corona_testing'
        }
        return all[acrnm] if acrnm else all
    
from datetime import datetime 

class ParticipantsBuilder:
    
    def __init__(self, study, participants_df, responses_df):
        self.study = study
        self.responses_df = responses_df.copy()
        self.participants_df = participants_df.copy()
        self._add_enroled_time()
            
    def _add_enroled_time(self):
        result = self.responses_df[self.responses_df['QUESTIONNAIRE'] == self.study.demographic()]
        result = result.sort_values('AUTHORED', ascending=False).drop_duplicates(['ALP_ID'])[['ALP_ID', 'AUTHORED']]  
        result.columns = ['ALP_ID', 'ENROLED_ON']
        self.participants_df = pd.merge(self.participants_df, result, how='left', on='ALP_ID')
        return self
    
    def add_last_donation(self):
        if 'LAST_DONATION' in self.participants_df.columns: return self
        result = self.responses_df.groupby('ALP_ID')
        result = result.agg({'AUTHORED': ['max']})
        result = result.reset_index()
        result.columns = ['ALP_ID', 'LAST_DONATION']
        self.participants_df = pd.merge(self.participants_df, result, how='left', on='ALP_ID')
        return self

    def add_all_submissions(self):
        questionnaires = self.study.questionnaires()
        self.participants_df['all'] = 0
        for acrnm in questionnaires.keys():
            self.add_submissions(questionnaires[acrnm], acrnm)
            self.participants_df['all'] = self.participants_df['all'] + self.participants_df[acrnm]
        return self
        
    def add_submissions(self, questionnaire_name, column_name=None):
        column_name = column_name or questionnaire_name
        df = self.responses_df[self.responses_df['QUESTIONNAIRE'] == questionnaire_name].copy()
        df['UNIQUE_QUESTIONNAIRE'] = df['AUTHORED'].dt.strftime("%Y%m%d") + df['QUESTIONNAIRE']
        result = df.groupby('ALP_ID')
        result = result.agg({'UNIQUE_QUESTIONNAIRE': ['nunique']})
        result.columns = [column_name]
        result.reset_index(inplace=True)
        result = pd.merge(self.participants_df, result, how='left', on='ALP_ID')
        result[column_name] = result[column_name].fillna(0).astype(int)
        self.participants_df = result
        return self
 
    def add_choice(self, questionnaire, question, column_name):
        self.add_answer(questionnaire, question, column_name, True)
        return self

    def add_answer(self, questionnaire, question, column_name, multichoice=False):
        r = self.responses_df
        df = r[(r['QUESTIONNAIRE'] == questionnaire) & (r['LINK_ID'] == question)] \
            if questionnaire \
            else r[r['LINK_ID'] == question]
        value_col = 'VALUECODING_CODE' if multichoice else 'VALUE'
        # use only the last submitted answer 
        df = df.sort_values('AUTHORED', ascending=False).drop_duplicates(['ALP_ID'])
        df = df[['ALP_ID', value_col]] # rename the value column
        df.columns = ['ALP_ID', column_name]
        self.participants_df = pd.merge(self.participants_df, df, how='left', on='ALP_ID')
        return self
    
    def filter_data4life_users(self):
        df = self.participants_df
        self.participants_df = df[~df['EXTERNAL_ID'].str.startswith('Data4Life', na=False)].reset_index(drop=True)
        return self
        
    def filter_annonymous_users(self):
        df = self.participants_df
        self.participants_df = df[df['EXTERNAL_ID'] != 'anonymous']
        return self

    def _filter_by_ids(self, users_ids):
        self.participants_df = self.participants_df[self.participants_df['ALP_ID'].isin(users_ids)].reset_index(drop=True)
        
    def filter_enrolled_before(self, day):
        self.participants_df = self.participants_df[self.participants_df['ENROLED_ON'] < day].copy()
        return self
        
    def filter_enrolled_after(self, day):
        self.participants_df = self.participants_df[self.participants_df['ENROLED_ON'] >= day].copy()
        return self

    def filter_acitve_beyond(self, days):
        self.add_last_donation()
        df = self.participants_df
        df = df[(df['LAST_DONATION'] - df['ENROLED_ON']).dt.days.fillna(0).astype(int) > days]
        self.participants_df = df.drop(columns=['LAST_DONATION'])
        return self
    
    def get(self):
        return self.participants_df.copy()