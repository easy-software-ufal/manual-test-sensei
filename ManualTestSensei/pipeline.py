import sys

import spacy
from collections import namedtuple
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

Test = namedtuple('Test', ['file', 'header', 'steps'])
Step = namedtuple('Step', ['action', 'reactions'])

def simplify_test(test:Test):
    return [simplify_step(step) for step in test.steps]

def simplify_step(step:Step):
    action = step.action.text
    reactions = '\n\n'.join([reaction.text for reaction in step.reactions])
    return Step(action, reactions)