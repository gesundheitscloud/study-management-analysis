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
    
study_ids = {
    'accept': 'fb4269d3-f6ac-4f81-85da-b80ce277793e',
    'cronos': '38ce29c0-eb76-45cc-ba4f-56395f8c49e0',
    'waiting_list': '3ce0e946-2aff-4960-aaca-d7fa43bdcc8e',
    'ecov': 'f875fdc4-c180-45f3-bdbb-a68fb1476338',
    'rki_panel': '0e858bc9-3be8-4d44-9139-97e6e678a334',
    'rki_feasibility': '5186aa14-9fcd-4742-b613-db6650c7cf0f',
    'femfit': '69990b1e-3b4c-4e7f-9d06-84cc2cdf88d0',
    'broad_consent': '1b29380e-dfd2-4ada-b7cc-a6d8575a631d',
    'user_research': 'f5a95a40-ccaa-4aec-bfec-c1a634e3a9a8',
    # Old studies
    'cocomo': 'e14cc34d-b78e-46ad-a7c6-f6159f1f1c96',
    'vaccine_effectiveness': 'e2ff06fc-18da-49b7-826e-d198c239ac6a'  
}
        
class Settings():
    def __init__(self, study_id, has_config=False):
        self.study_id = study_id
        self.has_config = has_config
    def get_study(self):
        return self.study_id
    def get_config(self):
        # DEFAULT_CONFIG = '92d7c6f8-3118-4256-ab22-f2f7fd19d4e7'
        DEFAULT_CONFIG = '903012b3-7c7b-4c96-a5b9-af38914b04b7'
        return DEFAULT_CONFIG if self.has_config else None

class SchemaManager():
    all_settings = {}
    all_settings[Schema.ACCEPT] = Settings(study_ids['accept'], True)
    all_settings[Schema.CRONOS] = Settings(study_ids['cronos'], True)
    all_settings[Schema.WAITING_LIST] = Settings(study_ids['waiting_list'], True)
    all_settings[Schema.ECOV] = Settings(study_ids['ecov'], True)
    all_settings[Schema.RKI_PANEL] = Settings(study_ids['rki_panel'], True)
    all_settings[Schema.RKI_FEASIBILITY] = Settings(study_ids['rki_feasibility'], True)
    all_settings[Schema.FEMFIT] = Settings(study_ids['femfit'], True)
    all_settings[Schema.BROAD_CONSENT] = Settings(study_ids['broad_consent'], True)
    all_settings[Schema.USER_RESEARCH] = Settings(study_ids['user_research'], True)

    @staticmethod
    def get_settings(schema_enum):
        return SchemaManager.all_settings[schema_enum]