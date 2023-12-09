from pipeline import Test, nlp
import smells_names
from matchers import helpers
from matchers_factory import MatchersFactory

class MisplacedAction:
    def __call__(self, test: Test) -> list[Test]:
        '''
        Steps usually come on the imperative format. Imperative sentences usually start with a verb in second person.
        https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
        This function checks if one of the steps of a test is an imperative sentence.
        '''
        matcher = MatchersFactory.misplaced_action_matcher()
        for (step_index, st) in enumerate(test.steps):
            for (reaction_index, reaction) in enumerate(st.reactions):
                reaction_matches = matcher(reaction)
                for (match_id, start, end) in reaction_matches:
                    helpers._store_smell(st, smells_names.MISPLACED_STEP, 'Transformed misplaced action. Location', 'verification', reaction[start:end])
                    new_action = test.steps[step_index].action.text+'. '+reaction.text
                    test.steps[step_index].action = nlp(new_action)
                    test.steps[step_index].reactions.pop(reaction_index)
        return [test, ]