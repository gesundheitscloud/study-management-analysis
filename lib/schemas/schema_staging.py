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
    'accept': 'a0cd02ce-6d1b-49f3-bc0e-14590c0249b3',
    'cronos': '5bc6be3d-1893-42ab-983c-b322f3daffe0',
    'waiting_list': '427f7191-7458-49d3-8dc1-36a230f586c3',
    'ecov': '686d3b9b-b8fd-46ba-9e25-af48c027bb55',
    'rki_panel': 'c9d45728-f720-45c6-b0ad-fd841f309c11',
    'rki_feasibility': '752e78e3-4be7-444d-bc59-766e6acd757e',
    'vaccine_effectiveness': 'e2ff06fc-18da-49b7-826e-d198c239ac6a',
    'femfit': '3506d0d0-0c67-4983-b9ce-b4d0ea8daeac',
    'broad_consent': '1b29380e-dfd2-4ada-b7cc-a6d8575a631d',
    'user_research': '9bf1a58d-85ba-4461-a46f-c8ca2a7bc1a3'
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
    

