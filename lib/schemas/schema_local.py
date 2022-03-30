from enum import Enum

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
        
class Settings():
    def __init__(self):
        self.study_id = 'this-is-dummy-id'
        self.has_config = True
    def get_study(self):
        return self.study_id
    def get_config(self):
        DEFAULT_CONFIG = 'this-is-dummy-config'
        return DEFAULT_CONFIG if self.has_config else None

class SchemaManager():

    @staticmethod
    def get_settings(schema_enum):
        return SchemaManager.Settings()