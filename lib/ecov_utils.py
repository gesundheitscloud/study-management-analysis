import calendar
import pandas as pd
from datetime import datetime, timedelta
from display import Display
from study import EcovStudy, ParticipantsBuilder

class ResponsesBuilder():
    def __init__(self, responses_df):
        self.study = EcovStudy()
        self.responses_df = responses_df.copy()

    def _filter_by_question(self, question_id, survey_id = None):
        condition = (self.responses_df['LINK_ID'] == question_id)
        if survey_id:
            condition = condition & (self.responses_df['QUESTIONNAIRE'] == survey_id) 
        return self.responses_df[condition]

    def get_answer(self, column_name, question_id, survey_id = None, multichoice=False):
        value_col = 'VALUECODING_CODE' if multichoice else 'VALUE'
        df = self._filter_by_question(question_id, survey_id)
        df = df.rename(columns={value_col: column_name})
        df = df[['ALP_ID', column_name, 'INTERACTION_ID', 'AUTHORED', 'QUESTIONNAIRE']]
        return df

    def get_choice(self, column_name, question_id, survey_id = None):
        return self.get_answer(column_name, question_id, survey_id, multichoice=True)


class TestManager():
    def __init__(self, responses_df):
        self.rb = ResponsesBuilder(responses_df)
        self._add_test_dates()
        self._add_method()
        self._add_result()
        self._add_test_profile()
        self._remove_duplications()
        
    def _add_test_dates(self):
        self.tests = pd.concat([
            self.rb.get_answer('TEST_DATE', 'when_tested'),
            self.rb.get_answer('TEST_DATE', 'when_tested_on_demand')
        ])
        self.tests['TEST_DATE'] = pd.to_datetime(self.tests['TEST_DATE'], format='%Y-%m-%d', errors='coerce')
    
    def _add_method(self):
        df = self.rb.get_choice('METHOD', 'what_test_method')
        self.tests = pd.merge(self.tests, df, how='left', on=['ALP_ID', 'INTERACTION_ID', 'AUTHORED', 'QUESTIONNAIRE'])
        
    def _add_result(self):
        df = self.rb.get_choice('RESULT', 'corona_test_result')
        self.tests = pd.merge(self.tests, df, how='left', on=['ALP_ID', 'INTERACTION_ID', 'AUTHORED', 'QUESTIONNAIRE'])

    def _add_test_profile(self):
        df = self.rb.get_choice('TEST_PROFILE', 'regular_testing')[['ALP_ID', 'TEST_PROFILE']].drop_duplicates()
        self.tests = pd.merge(self.tests, df, how='left', on=['ALP_ID'])

    def _remove_duplications(self):
        self.tests.sort_values(['AUTHORED', 'INTERACTION_ID'], inplace = True) 
        self.tests = self.tests.drop_duplicates(['ALP_ID', 'TEST_DATE'], keep='last')
        
    def get(self):
        df = self.tests.drop(columns=['INTERACTION_ID'])
        return df
    
    def count_participants(self, min_number_of_tests):
        df = self.tests.groupby('ALP_ID').agg({'TEST_DATE' : ['count']})
        df.reset_index(inplace=True)
        df.columns = ['ALP_ID', 'COUNT']
        df = df[df['COUNT'] >= min_number_of_tests]
        return len(df['ALP_ID'].unique())
    
class DaysCounter():
    @staticmethod
    def weekday_count(start_date, end_date):
        # input: datetime
        # return: {'Monday': 15, 'Tuesday': 14, 'Wednesday': 14, 'Thursday': 14, 'Friday': 14, 'Saturday': 14, 'Sunday': 14}
        week = {}
        for i in range((end_date - start_date).days + 1):
            day       = calendar.day_name[(start_date + timedelta(days=i)).weekday()]
            week[day] = week[day] + 1 if day in week else 1
        return week

    @staticmethod
    def wednesday_count(start_date, end_date):
        WED = 'Wednesday'
        week = DaysCounter.weekday_count(start_date, end_date) 
        return week[WED] if WED in week.keys() else 0

    @staticmethod
    def wednesday_count_wrapper(start, end):
        if pd.isnull(start): return 0
        start_date = start.to_pydatetime()
        end_date = end.to_pydatetime()
        return DaysCounter.wednesday_count(start_date, end_date)
    
class Vaccination:
    def __init__(self, participants_df, responses_df):
        self.df = self._build_frame(participants_df, responses_df)
        self.tests = self._build_tests_with_vaccine_status(responses_df)

    def _build_frame(self, participants_df, responses_df):
        df = ParticipantsBuilder(EcovStudy(), participants_df, responses_df) \
        .add_choice('covid_first_vaccine', 'corona_vaccination_received', '1ST_DOSE') \
        .add_choice('covid_first_vaccine', 'which_vaccine_received', '1ST_VACCINE_TYPE') \
        .add_answer('covid_first_vaccine', 'when_vaccinated_first_time', '1ST_VACCINE_DATE') \
        .add_choice('covid_second_vaccine','has_received_second_vacciation', '2ND_DOSE') \
        .add_choice('covid_second_vaccine', 'which_vaccine_received', '2ND_VACCINE_TYPE') \
        .add_answer('covid_second_vaccine', 'when_vaccinated_second_time', '2ND_VACCINE_DATE') \
        .add_last_donation() \
        .get()

        df['1ST_VACCINE_DATE'] = pd.to_datetime(df['1ST_VACCINE_DATE'], format='%Y-%m-%d', errors='coerce')
        df['2ND_VACCINE_DATE'] = pd.to_datetime(df['2ND_VACCINE_DATE'], format='%Y-%m-%d', errors='coerce')
        return df
        
    def get_frame(self):
        return self.df
    
    def get_tests(self):
        return self.tests
    
    def get_vaccine_status(self, day):
        return pd.DataFrame(data={
            'status': self.df.apply(lambda row : self._vaccine_status_on_date(day, row), axis=1), 
            'type': self.df.apply(lambda row : self._vaccine_type_on_date(day, row), axis=1)
        })
        
    def _build_tests_with_vaccine_status(self, responses_df):
        tests = TestManager(responses_df).get()
        tests = tests[tests['AUTHORED'] >= datetime(2017,1,1)]
        tests['VACCINE_STATUS'] = tests.apply(lambda row : self._vaccine_status_on_test_date(row), axis=1)
        tests['VACCINE_TYPE'] = tests.apply(lambda row : self._vaccine_type_on_test_date(row), axis=1)
        return tests
        
    def _vaccine_status_on_test_date(self, test_row):
        date = test_row['TEST_DATE']
        vaccine_row = self.df[self.df['ALP_ID'] == test_row['ALP_ID']].iloc[0]
        return self._vaccine_status_on_date(date, vaccine_row)

    def _vaccine_type_on_test_date(self, test_row):
        date = test_row['TEST_DATE']
        vaccine_row = self.df[self.df['ALP_ID'] == test_row['ALP_ID']].iloc[0]
        return self._vaccine_type_on_date(date, vaccine_row)
    
    def _vaccine_status_on_date(self, date, row):
        if pd.isnull(date): return 'UNKNOWN'
        dose1_occured = row['1ST_DOSE']
        dose1_date = row['1ST_VACCINE_DATE']
        dose1_type = row['1ST_VACCINE_TYPE']
        dose2_occured = row['2ND_DOSE']
        dose2_date = row['2ND_VACCINE_DATE']
        dose2_type = row['2ND_VACCINE_TYPE'] 

        if ((dose1_occured == 'yes') & pd.isna(dose1_date)) | ((dose2_occured == 'yes') & pd.isna(dose2_date)):
            return 'UNKNOWN'

        if (dose1_occured != 'yes') or (date < dose1_date):
            return 'NOT-VACCNIATED'

        if (dose2_occured == 'yes') & (date >= dose2_date):
            return 'FULLY'

        if dose1_type in ['johnson']: return 'FULLY' 
        if dose1_type in ['pfizer', 'moderna', 'astra_zeneca', 'sputnik']: return 'PARTIALLY' 
        return 'UNKNOWN'

    def _vaccine_type_on_date(self, date, row):
        status = self._vaccine_status_on_date(date, row)
        
        import numpy as np
        if status != 'FULLY': return np.nan

        dose1_type = row['1ST_VACCINE_TYPE']
        if (dose1_type in ['johnson']):
            return dose1_type
        
        dose2_type = row['2ND_VACCINE_TYPE']
        if (dose1_type == 'other') | (dose2_type == 'other'): return 'other'
        if (dose1_type == dose2_type): return dose1_type
        return 'mixed'
