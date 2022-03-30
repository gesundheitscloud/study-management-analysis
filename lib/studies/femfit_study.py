from ..study import Study

class FemfitStudy(Study):    
    
    def name(self):
        return "FeMFit"
    
    def demographic(self):
        return self.questionnaires()['Q1']
    
    def questionnaires(self):
        return {
            'Q1': 'Q1_personal_info', 
            'Q2': 'Q2_physical_wellbeing_and_activity',
            'Q3': 'Q3_cycle_dependent',
            'Q4': 'Q4_final_app_rating',
            'Q5': 'Q5_leaving_study'
        }