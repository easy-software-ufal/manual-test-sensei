import sys
from itertools import chain
import collections
import copy

import spacy
from dataclasses import dataclass, field
import logging
log = logging.getLogger(__name__)




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
        return f'{self.hint}: \'{self.where}\''

class Memento:
    '''Implements the memento design pattern'''
    def __init__(self):
        self._snapshots = list()

    def take_snapshot(self) -> bool:
        '''Stores the current state of the memento into the attribute self.snapshots'''
        if not self._snapshots:
            self._snapshots = list()
        snapshot = copy.deepcopy(self)
        self._snapshots.append(snapshot)
        return True

    def rollback(self):
        if self._snapshots:
            return self._snapshots[-1]
        return None

    def rollback_all(self):
        yield self
        r = self.rollback()
        while r:
            yield r
            r = r.rollback()

    def _get_attributes_names(self) ->list[str]:
        names = [name for name in dir(self) if not name.startswith('_') and not callable(getattr(self, name))]
        return names

class Step(Memento):
    def __init__(self, action:str='', reactions:list = None, where:str='', smells:list = None):
        super().__init__()
        self.action = action
        self.where = where
        self._flags=list()
        if reactions:
            self.reactions = reactions
        else:
            self.reactions = list()
        if smells:
            self.smells = smells
        else:
            self.smells = list()

    def add_flag(self, flag:str) -> bool:
        self._flags.append(flag)
        return True

    def has_flag(self, flag:str) -> bool:
        return flag in self._flags


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
    header = ['* '+t for t in test.header if len(t) > 0]
    return [header, simplified]

def simplify_step(step:Step):
    action = step.action.text
    reactions = '\n\n'.join([reaction.text for reaction in step.reactions])
    smells = ' | '.join([str(smell) for smell in step.smells])
    if not smells:
        smells = '-'
    return {'action':action, 'verifications':reactions, 'hints':smells}

if __name__ == '__main__':
    st1 = Step('step0', ['testando'], 'step1', ['testando isso'])
    tt1 = Test('abc.txt', ['teste1'], [st1])
    tt1.take_snapshot()
    tt1.steps[0] = Step('step1', ['testando'], 'step1', ['testando isso'])
    tt1.take_snapshot()
    tt1.steps[0] = Step('step2', ['testando'], 'step1', ['testando isso'])
    tt1.take_snapshot()
    tt1.steps[0] = Step('step3', ['testando'], 'step1', ['testando isso'])
    tt1.take_snapshot()
    tt1.steps[0] = Step('step4', ['testando'], 'step1', ['testando isso'])
    # [print(t.steps[0].action) for t in tt1.rollback_all()]
    for tt in tt1.rollback_all():
        print(tt.steps[0].action)