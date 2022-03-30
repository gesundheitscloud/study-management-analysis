from datetime import datetime
from numpy import random

import math
import time
import pandas as pd

def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(time_format, time.localtime(ptime))

class SurveyGenerator():

    def __init__(self, template_reader):
        self.reader = template_reader
        columns = ['ALP_ID','VERSION', 'QUESTIONNAIRE', 'STATUS', 'AUTHORED', 
                   'LINK_ID', 'VALUE', 'VALUECODING_CODE', 'LANGUAGE', 'TEXT', 'QUESTIONNAIRE_ID']
        self.responses_df = pd.DataFrame(columns=columns)
        self.count_surveys = 0
        participants_columns = 'ALP_ID', 'EXTERNAL_ID', 'STATUS', 'START_DATE', 'END_DATE'
        self.participants_df = pd.DataFrame(columns=participants_columns)
        
    def create_participants(self, total_amount, suspended_amount):
        if suspended_amount > total_amount: 
            raise ValueError("suspended amount needs to be smaller than total amount")
    
        for i in range(total_amount):
            enrolled = (i >= suspended_amount)
            is_tester = i % 5 == 0
            user = EnroledUser(enrolled, is_tester)
            self.participants_df = self.participants_df.append(user.to_json(), ignore_index=True)
            self.add_survey(user.id, user.enroled_on, False)

    @staticmethod
    def random_month(prop, start="1900-01", end=None):
        end = datetime.today().strftime('%Y-%m') if not end else end
        return str_time_prop(start, end, '%Y-%m', prop)

    @staticmethod
    def random_string(length):
       return ''.join(random.choice(string.lowercase) for i in range(length))

    def select_answer(self, answer_type, answer_set_id, range_id):
        if answer_type in ['Single select', 'Multi select']:
            choices = self.reader.answer_sets[answer_set_id]
            return random.choice(choices)
        if answer_type == 'Month':
            return SurveyGenerator.random_month(random.random())
        if isinstance(range_id, str):
            r = self.reader.ranges[range_id]
            # --- normal distribution ---
            value = int(random.normal(loc=(r.min + r.max)/2, scale=(r.max - r.min)/6))
            # --- uniform distribution ---
            # value = random.randint(r.min, r.max)
            if r.type == 'Integer': return value
            if r.type == 'String': return SurveyGenerator.random_string(value)
            raise ValueError(f'Range type {r.type} is invalid') 
        raise ValueError(f'Cannot select an answer for {answer_type}, {answer_set_id}, {range_id}')

    def is_fulfilled(self, df, condition_id):
        if not isinstance(condition_id, str): return True
        cond = self.reader.conditions[condition_id]
        prev_answer = df[df['LINK_ID'] == cond.question_id]['VALUECODING_CODE'].iloc[0]
        return prev_answer in cond.answer_ids

    def add_survey(self, user_id, submitted_on, is_english):
        language = 'English' if is_english else 'German'
        df = self.reader.get_program().rename(columns={
            'Questionnaire Name': 'QUESTIONNAIRE',
            'Question Name': 'LINK_ID',
            language: 'TEXT'})

        answers_series = df.apply(lambda row : self.select_answer(
            row['Answer Type'], row['Answers'], row['Range']
        ), axis = 1)

        indexes = df['Answer Type'].isin(['Single select', 'Multi select'])
        df.loc[indexes, 'VALUECODING_CODE'] = answers_series
        df.loc[~indexes, 'VALUE'] = answers_series

        df['ALP_ID'] = user_id
        df['VERSION'] = '1.0.0'
        df['STATUS'] = 'completed'
        df['LANGUAGE'] = 'en' if is_english else 'de'
        df['AUTHORED'] = submitted_on
        df['QUESTIONNAIRE_ID'] = f'{self.count_surveys + 1}'
        self.count_surveys = self.count_surveys + 1

        # --- test conditions: gesundheitsberufe, hochschule
        # df.loc[df['LINK_ID'] == 'HBA1A', 'VALUECODING_CODE'] = 'gesundheitsberufe'
        df = df[df.apply(lambda row : self.is_fulfilled(df, row['Condition']), axis = 1)]
        
        columns=['Order', 'Required', 'Condition', 
                 'Info (German)', 'Info (English)', 
                 f'{"German" if is_english else "English"}',
                 'Answer Type', 'Answers', 'Range']
        
        df.drop(columns=columns, inplace=True)
        self.responses_df = self.responses_df.append(df, ignore_index=True)

    def get_participants(self):
        return self.participants_df \
            .sort_values(by=['START_DATE']) \
            .reset_index(drop=True)

    def get_responses(self):
        return self.responses_df
    

class EnroledUser():
    
    next_id = 1000
    count = 1
    
    def __init__(self, enrolled=True, is_tester=False):
        self.id = EnroledUser.generate_user_id()
        self.enroled_on = EnroledUser.get_authored_date()
        self.enrolled = enrolled
        self.external_id = EnroledUser.get_external_id(is_tester)
        
    def to_json(self):
        return {
            'ALP_ID': self.id, 
            'EXTERNAL_ID': self.external_id,
            'STATUS': f'{"enrolled" if self.enrolled else "suspended"}',
            'START_DATE': self.enroled_on,
            'END_DATE': f'{pd.NaT if self.enrolled else datetime.today().strftime("%Y-%m-%d")}'
        }
        
    @staticmethod
    def generate_user_id():
        EnroledUser.next_id += 1
        return str(EnroledUser.next_id)
#         import rstr
#         return rstr.xeger(r'[0-9]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\Z')

    @staticmethod
    def get_authored_date(start_from='2021-01-01'):
        today = datetime.today().strftime('%Y-%m-%d')
        return str_time_prop(start_from, today, '%Y-%m-%d', random.random())
    
    @staticmethod
    def get_external_id(is_tester):
        identifier = EnroledUser.count * 5 + 2
        EnroledUser.count += 1
        return f'test_user_{identifier}' if is_tester else f'uninklinik_{identifier}'
    