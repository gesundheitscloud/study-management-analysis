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
