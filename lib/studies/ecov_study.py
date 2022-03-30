from ..study import Study

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
