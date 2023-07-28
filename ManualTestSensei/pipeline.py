import sys
from itertools import chain
import collections
import copy

import spacy
from dataclasses import dataclass, field
import logging
log = logging.getLogger(__name__)


# TODO: Turn it into a singleton

try:
    if sys.argv[1] == 'english' or sys.argv[1] == 'trf':
        model = 'en_core_web_trf'
    elif sys.argv[1] == 'small' or sys.argv[1] == 'en_core_web_sm':
        model = 'en_core_web_sm'
    else:
        model = 'en_core_web_sm'
except IndexError:
    model = 'en_core_web_lg'  # Development only

nlp = spacy.load(model)

lang = nlp.meta['lang']
name = nlp.meta['name']
model_name = lang + '_' + name
log.info(f'spaCy model: {model_name}')

# Test = namedtuple('Test', ['file', 'header', 'steps', 'smell', 'where', 'term', 'action'])
# Step = namedtuple('Step', ['action', 'reactions', 'smell', 'where', 'term'])

@dataclass
class Smell:
    smell : str = field(default=None)
    where : str = field(default=None)
    hint : str = field(default=None)
    term : str = field(default=None)

    def __str__(self):
        return f'{self.smell} ({self.hint})\nLocation: {self.where} | Term: {self.term}'

class Memento:
    '''Implements the memento design pattern'''
    def __init__(self):
        self._snapshots = list()

    def take_snapshot(self) -> bool:
        '''Stores the current state of the memento into the attribute self.snapshots'''
        if not self._snapshots:
            self._snapshots = list()
        snapshot = copy.copy(self)
        attribute_names = self._get_attributes_names()
        for name in attribute_names:
            attribute_value = getattr(self, name)
            if isinstance(attribute_value, collections.abc.Sequence) and not isinstance(attribute_value, str):
                for inner_attribute_value in attribute_value:
                    inner_attribute_value.take_snapshot()
        self._snapshots.append(snapshot)
        return True

    def rollback(self):
        try:
            last_snapshot = self._snapshots.pop()
        except IndexError: #There are no snapshots
            return None
        attribute_names = self._get_attributes_names()
        for name in attribute_names:
            attribute_value = getattr(self, name)
            if isinstance(attribute_value, collections.abc.Sequence) and not isinstance(attribute_value, str):
                values = (inner_value.rollback()  for inner_value in attribute_value)
                values = [v for v in values if v is not None]
                setattr(self, name, values)
            else:
                setattr(self, name, getattr(last_snapshot, name))
        return self

    def _get_attributes_names(self) ->list[str]:
        names = [name for name in dir(self) if not name.startswith('_') and not callable(getattr(self, name))]
        return names

class Step(Memento):
    def __init__(self, action:str='', reactions:list = None, where:str='', smells:list = None):
        super().__init__()
        self.action = action
        self.where = where
        if reactions:
            self.reactions = reactions
        else:
            self.reactions = list()
        if smells:
            self.smells = smells
        else:
            self.smells = list()


class Test(Memento):
    def __init__(self, file:str, header:str, steps:list=None, smells:list=None):
        super().__init__()
        self.file = file
        self.header = header
        if steps:
            self.steps = steps
        else:
            self.steps = list()
        if smells:
            self.smells = smells
        else:
            self.smells = list()

    def get_smells(self) -> list:
        smells = list()
        smells = smells + self.smells
        steps_smells = [step.smells for step in self.steps if st.smells]
        smells = smells + steps_smells
        return list(chain(*smells))


def simplify_test(test:Test):
    simplified = [simplify_step(step) for step in test.steps]
    return simplified

def simplify_step(step:Step):
    action = step.action.text
    reactions = '\n\n'.join([reaction.text for reaction in step.reactions])
    smells = '\n'.join([str(smell) for smell in step.smells])
    if not smells:
        smells = '-'
    return {'action':action, 'expected results':reactions, 'smells':smells}

if __name__ == '__main__':
    st = Step('primeiro_action', list(), 'primeiro_where', list())
    st.take_snapshot()
    st.action = 'segundo_action'
    print(st.action)
    print(st.rollback().action)