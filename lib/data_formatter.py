import pandas as pd
from lib.participant_builder import ParticipantsBuilder
from lib.response_builder import ResponsesBuilder

class DataFormatter():
    def __init__(self, study, p_df, r_df):
        self.study = study
        self.p_df = p_df
        self.r_df = DataFormatter._clean_and_order(r_df)
        self.tranlation_dict = {}

    class Question():
        def __init__(self, questionnaire_name, question_id, is_choice):
            self.questionnaire_name = questionnaire_name
            self.question_id = question_id
            self.is_choice = is_choice

        def get_values(self, responses_builder, column_name):
            df = responses_builder.get_answer(column_name, self.question_id, self.questionnaire_name, self.is_choice)
            return df[['ALP_ID', column_name]]

    def _create_questions_list(self, questionnaire_name):
        filtered_responses = self.r_df[(self.r_df['QUESTIONNAIRE'] == questionnaire_name)]
        questions_ids = filtered_responses['LINK_ID'].unique()
        questions = []
        for q_id in questions_ids:
            s = self.r_df[self.r_df['LINK_ID'] == q_id].iloc[0]  
            q = DataFormatter.Question(questionnaire_name, q_id, pd.isna(s['VALUE']))
            questions.append(q)
        return questions

    @staticmethod
    def _create_instance_answers(r_df, questions, prefix):
        r = ResponsesBuilder(r_df)
        result = None
        for q in questions:
            column_name = f'{prefix}{q.question_id}'
            temp = q.get_values(r, column_name)
            result = temp if result is None else pd.merge(result, temp, how='left', on='ALP_ID')
        return result    
        
    def add_translation_table(self, tranlation_dict):
        self.tranlation_dict = tranlation_dict
        return self
        
    def questionanires_ids(self):
        return self.r_df['QUESTIONNAIRE'].unique()

    def reoccuring_questionanires_ids(self):
        df = self.r_df.groupby(['ALP_ID', 'QUESTIONNAIRE'])['AUTHORED'].unique().to_frame().reset_index()
        df['size'] = df['AUTHORED'].apply(lambda x: len(x))
        reoccuring_questionnaires = df[df['size'] > 1]['QUESTIONNAIRE'].unique()
        return reoccuring_questionnaires

    def create_questionnaire_answers(self, questionnaire_name):
        users_df = ParticipantsBuilder(self.study, self.p_df, self.r_df).get()
        r_df = self.r_df[(self.r_df['QUESTIONNAIRE'] == questionnaire_name)].copy()
        questions = self._create_questions_list(questionnaire_name)
        loops = r_df['INSTANCE'].max()
        loops = 0 if pd.isnull(loops) else loops
        users_df['SUBMISSIONS'] = 0
        for i in range(1, loops + 1):
            prefix = f'{i}_' if loops > 1 else ''
            df = r_df[r_df['INSTANCE'] == i]
            # Display.frame(df.drop(columns=['QUESTIONNAIRE_ID']))
            result = df[['ALP_ID', 'AUTHORED']].drop_duplicates().rename(columns = {'AUTHORED': f'{prefix}AUTHORED'})
            users_df = pd.merge(users_df, result, how='left', on='ALP_ID')
            result = DataFormatter._create_instance_answers(df, questions, prefix).replace(self.tranlation_dict)
            users_df = pd.merge(users_df, result, how='left', on='ALP_ID')
            users_df['SUBMISSIONS'] += users_df[f'{prefix}AUTHORED'].notnull().astype(int)
        
        u = users_df.select_dtypes(include=['datetime'])
        users_df[u.columns] = u.fillna('')
        return users_df

    @staticmethod
    def _clean_and_order(r_df):
        r_df = r_df[~pd.isnull(r_df['LINK_ID'])]
        r_df = r_df.sort_values(by=['ALP_ID', 'QUESTIONNAIRE', 'AUTHORED', 'QUESTIONNAIRE_ID'])
        # Remove same quesitonnaires submitted on the exact same date
        r_df['DUPLICATE'] = r_df.groupby(['ALP_ID', 'QUESTIONNAIRE', 'AUTHORED'])['QUESTIONNAIRE_ID'] \
            .transform(lambda x: (x!=x.shift()).cumsum())
        r_df = r_df[r_df['DUPLICATE'] == 1].drop(columns=['DUPLICATE'])
        # Add instance number
        r_df['INSTANCE'] = r_df.groupby(by=['ALP_ID', 'QUESTIONNAIRE'])['AUTHORED'] \
                .transform(lambda x: (x!=x.shift()).cumsum())
        return r_df
