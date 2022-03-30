from ..study import Study

class RkiPanelStudy(Study):    
    
    def name(self):
        return "RKI Panel"
    
    def demographic(self):
        return self.questionnaires()['Q1']
    
    def questionnaires(self, acrnm=None):            
        all = {
            'Q1' : 'S1'
        }
        return all[acrnm] if acrnm else all
    
