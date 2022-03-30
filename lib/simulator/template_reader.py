import csv
import pandas
import pandas as pd
import rstr
from IPython.display import display, HTML

class Condition():
    def __init__(self, row):
        self.question_id = row[1]
        self.answer_ids = list(filter(None, row[2:]))
    def __repr__(self):
        return f'Condition(question_id={self.question_id}, answer_ids={self.answer_ids})'
    def __str__(self):
        return f'Condition has question_id {self.question_id} and answer_ids {self.answer_ids}'

class Range():
    def __init__(self, row):
        self.type = row[1]
        self.min = int(row[2]) if row[2].isnumeric() else None
        self.max = int(row[3]) if row[3].isnumeric() else None
    def __repr__(self):
        return f'Range(type={self.type}, min={self.min}, max={self.max})'
    def __str__(self):
        return f'Range has type {self.type}, min is {self.min} and max is {self.max})'
    
class TemplateReader():
        
    def __init__(self, base_path, folder_name):
        self._find_base_path(base_path, folder_name)
        questionnaires_df = pandas.read_csv(self.base_path + 'Questionnaires.csv', sep=',')
        questions_df = pandas.read_csv(self.base_path + 'Demographics.csv', sep=',')
        self.df = pandas.merge(questionnaires_df, questions_df, how='left', on='Question Name')
        self._create_answer_sets()
        self._create_answers()
        self._create_conditions()
        self._create_ranges()

    def _find_base_path(self, base_path, folder_name):
        import json
        with open(base_path + '/config.json', 'r') as f:
            files = json.load(f)
        self.base_path = files[folder_name]['template_dir']

    def _create_answer_sets(self):
        answer_sets = {}
        with open(self.base_path + 'AnswerSets.csv', mode='r') as infile:
            reader = csv.reader(infile)
            self.answer_sets = {rows[0]:list(filter(None, rows[1:])) for rows in reader}

    def _create_answers(self):
        answers = {}
        with open(self.base_path + 'Answers.csv', mode='r') as infile:
            reader = csv.reader(infile)
            header = next(reader)
            self.answers = {rows[0]:rows[2] for rows in reader}

    def _create_conditions(self):
        conditions = {} 
        with open(self.base_path + 'Conditions.csv', mode='r') as infile:
            reader = csv.reader(infile)
            header = next(reader)
            self.conditions = {row[0]: Condition(row) for row in reader}

    def _create_ranges(self):
        ranges = {}    
        with open(self.base_path + 'Ranges.csv', mode='r') as infile:
            reader = csv.reader(infile)
            header = next(reader)
            self.ranges = { row[0]: Range(row) for row in reader }
    
    def get_program(self):
        return self.df.copy()
        