from ..study import Study

class AcceptStudy(Study):    
    
    def name(self):
        return "Accept"
    
    def demographic(self):
        return self.questionnaires()['Q1']
    
    def questionnaires(self):
        return {
            'Q1': 'Q1', 
            'Q2': 'Q2',
            'Q3': 'Q3',
            'Q4a': 'Q4a',
            'Q4b': 'Q4b',
            'Q6': 'Q6',
            'Q7': 'Q7',
            'Q8': 'Q8',
            'Q9': 'Q9'
        }