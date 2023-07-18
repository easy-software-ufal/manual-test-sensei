import sys
from itertools import chain

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

@dataclass
class Step:
    action : str
    reactions : list[str]
    where : str = field(default=None)
    smells : list[Smell] = field(default_factory=list)


@dataclass
class Test:
    file : str
    header : str
    steps : list[Step]
    smells : list[Smell] = field(default_factory=list)

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