from collections import abc

import smells_names
import spacy
from matchers_factory import MatchersFactory
from pipeline import Test
from matchers import helpers
import smells_names

class ConditionalTestLogic:
    smell = smells_names.CONDITIONAL_TEST_LOGIC

    def __call__(self, test: Test):
        """
        Subordinate (dependent clauses). They start with a subordinating conjunction
        """
        matcher = MatchersFactory.conditional_test_matcher()
        for step in test.steps:
            # Actions
            action_matches = matcher(step.action)
            for match_id, start, end in action_matches:
                helpers._store_smell(step, self.smell, 'dependent clause', 'verification', step.action[start:end])
            #Reactions
            for reaction in step.reactions:
                reaction_matches = matcher(reaction)
                for match_id, start, end in reaction_matches:
                    helpers._store_smell(step, self.smell, 'dependent clause', 'verification', reaction[start:end])