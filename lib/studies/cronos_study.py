from ..study import Study

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
