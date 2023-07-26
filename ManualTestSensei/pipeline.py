import sys
from itertools import chain
import collections

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
        if self._snapshots:
            last_snapshot = self._snapshots[-1]
        else:
            last_snapshot = None
            self._snapshots = list()
        snapshot = self.__class__(self) # This is poorly optimized since it duplicates data, but we are dealing with few data.
        attribute_names = self._get_attributes_names()
        for name in attribute_names:
            attribute_value = getattr(self, name)
            if isinstance(attribute_value, collections.abc.Sequence) and not isinstance(attribute_value, str):
                for inner_attribute_value in attribute_value:
                    inner_attribute_value.take_snapshot()
        self._snapshots.append(snapshot)
        return True

    def rollback(self):
        data = self.__class__()
        last = self._snapshots[-1]
        attribute_names = self._get_attributes_names()
        for name in attribute_names:
            attribute_value = getattr(self, name)
            if isinstance(attribute_value, collections.abc.Sequence) and not isinstance(attribute_value, str):
                values = [inner_value.rollback()  for inner_value in attribute_value]
                setattr(data, name, values)
        return data

    def _get_attributes_names(self) ->list[str]:
        names = [name for name in dir(self) if not name.startswith('_') and not callable(getattr(self, name))]
        return names

class Step(Memento):
    def __init__(self, action:str='', reactions:list = None, where:str='', smells:list = None):
        super().__init__()
        self.action = action
        if reactions:
            self.reactions = reactions
        else:
            self.reactions = list()
        self.where = where
        self.smells = smells


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
            self.smells = list(0)

    def get_smells(self) -> list:
        smells = list()
        smells = smells + self.smells
        steps_smells = [step.smells for step in self.steps if step.smells]
        smells = smells + steps_smells
        return list(chain(*smells))


def simplify_test(test:Test):
    return [simplify_step(step) for step in test.steps]

def simplify_step(step:Step):
    action = step.action.text
    reactions = '\n\n'.join([reaction.text for reaction in step.reactions])
    smells = '\n'.join([str(smell) for smell in step.smells])
    if not smells:
        smells = '-'
    return Step(action, reactions, smells=smells)


if __name__ == '__main__':
    step = Step('a', list(), 'abc', list())
    print(step._get_attributes_names())
    step.take_snapshot()