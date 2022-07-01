class ResponsesBuilder():
    def __init__(self, responses_df):
        self.responses_df = responses_df.copy()

    def _filter_by_question(self, question_id, survey_id = None):
        condition = (self.responses_df['LINK_ID'] == question_id)
        if survey_id:
            condition = condition & (self.responses_df['QUESTIONNAIRE'] == survey_id) 
        return self.responses_df[condition]

    def get_eariest_responding_time(self, questionnaire_name, column_name):
        result = self.responses_df[self.responses_df['QUESTIONNAIRE'] == questionnaire_name]
        result = result[['ALP_ID', 'AUTHORED']]
        result = result.groupby(by=['ALP_ID']).agg({'AUTHORED': ['min']})
        result.reset_index(inplace=True)
        result.columns = ['ALP_ID', column_name]
        return result
    
    def get_answer(self, column_name, question_id, survey_id = None, multichoice=False):
        value_col = 'VALUECODING_CODE' if multichoice else 'VALUE'
        df = self._filter_by_question(question_id, survey_id)
        df = df.rename(columns={value_col: column_name})
        df = df[['ALP_ID', column_name, 'QUESTIONNAIRE_ID', 'AUTHORED', 'QUESTIONNAIRE']]
        return df

    def get_choice(self, column_name, question_id, survey_id = None):
        return self.get_answer(column_name, question_id, survey_id, multichoice=True)