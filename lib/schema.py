from enum import Enum
import json

class Schema(Enum):
    ACCEPT = 1
    CRONOS = 2
    COCOMO = 3
    WAITING_LIST = 4
    ECOV = 5
    RKI_PANEL = 6
    RKI_FEASIBILITY = 7
    FEMFIT = 8
    BROAD_CONSENT = 9
    USER_RESEARCH = 10
    SYMPTOM_TRACKER = 11
        
class Settings():
    def __init__(self, study_id, config_id):
        self.study_id = study_id
        self.config_id = config_id
    def get_study(self):
        return self.study_id
    def get_config(self):
        return self.config_id

class SchemaManager():
    @staticmethod
    def get_settings(schema_enum):
        with open(r'./config.json', "r") as jsonFile:
            data = json.load(jsonFile)
        env_name = data['env']
        if schema_enum.name not in data[env_name]:
            raise Exception('Study id is missing')
        study_id = data[env_name][schema_enum.name]
        config_id = data[env_name]['default_config']
        return Settings(study_id, config_id)