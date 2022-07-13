from ..study import Study

class SymptomTracker(Study):    
    
    def name(self):
        return "SymptomTracker"
    
    def demographic(self):
        return None
    
    def questionnaires(self):
        return {
            'symptoms': 'covid19-covhub-symptom-tracking', 
            'vaccine': 'vaccine_questionnaire',
            'test': 'post-covid19-test'
        }