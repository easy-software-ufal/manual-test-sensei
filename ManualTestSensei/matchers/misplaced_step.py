from pipeline import Test
import smells_names
from matchers import helpers

def find_misplaced_step(test: Test):
    '''
    Steps usually come on the imperative format. Imperative sentences usually start with a verb in second person.
    https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    This function checks if one of the steps of a test is an imperative sentence.
    '''
    matcher = MatchersFactory.misplaced_step_matcher()
    for step in test.steps:
        for reaction in step.reactions:
            reaction_matches = matcher(reaction)
            for match_id, start, end in reaction_matches:
                helpers._store_smell(step, smells_names.MISPLACED_STEP, '', 'verification', reaction[start:end])