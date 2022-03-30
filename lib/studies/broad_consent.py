from ..study import Study

class BroadConsent(Study):    
    
    def name(self):
        return "BroadConsent"
    
    def demographic(self):
        return self.questionnaires()['FeMFit_Q1']
    
    def questionnaires(self):
        return {
            'FeMFit_Q1': 'Q1_personal_info', 
            'FeMFit_Q2': 'Q2_physical_wellbeing_and_activity',
            'FeMFit_Q3': 'Q3_cycle_dependent',
            'FeMFit_Q4': 'Q4_final_app_rating',
            'FeMFit_Q5': 'Q5_leaving_study'
        }