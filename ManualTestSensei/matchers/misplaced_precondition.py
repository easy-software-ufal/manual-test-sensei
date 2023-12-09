from pipeline import Test, nlp
import smells_names
from matchers_factory import MatchersFactory
# from helpers import _store_smell
from itertools import product
import copy
from collections import Counter

_OPERATIONS = (_REMOVE:=0, _REFACTOR:=1)

class MisplacedPrecondition:
    smell:str = smells_names.MISPLACED_PRECONDITION
    _matcher = MatchersFactory.misplaced_precondition_matcher()

    def __call__(self, test: Test) -> list[Test]:
        """
            The first action step declares the SUT state (e.g. 'wifi is turned off')
        """

        for (step_index, st) in enumerate(test.steps):
            sentences = list(enumerate(st.action.sents))
            found_matches = False
            for (sentence_index, sent) in sentences[::]:
                if self._matcher(sent):
                    found_matches = True
                    sentences[sentence_index] = _REMOVE
                    test.header.append(str(sent))
            if found_matches:
                sentences = [str(sent[1]) for sent in sentences if sent != _REMOVE]
                if not sentences:
                    test.steps.pop(step_index)
                else:
                    test.steps[step_index].action = nlp(' '.join(sentences))
        return [test]

    # def _mark_step_to_deletion(self, test:Test, number_of_steps:int) -> Test:
    #         for step_index in range(number_of_steps):
    #             test.steps[step_index] = None
    #         return test

    # def count_smelly_steps(self, test : Test) -> int:
    #     '''
    #     Returns the truth table where each row indicates wheter a step will be removed or refactored.
    #     '''
    #     step_smells_map = list()
    #     for (index, st) in enumerate(test.steps):
    #         action_matches = self._matcher(st.action)
    #         if action_matches:
    #             step_smells_map.append(True)
    #         else:
    #             step_smells_map.append(False)

    #     counter = dict(Counter(step_smells_map))
    #     try:
    #         trues = counter[True]
    #     except KeyError:
    #         trues = 0

    #     return trues


    # def _refactor_test(self, test:Test, number_of_steps:int) -> Test:
    #     for step_index in range(number_of_steps):
    #         st = test.steps[step_index]
    #         # breakpoint()
    #         sents = [sent for sent in st.action.sents]
    #         for sent in sents:
    #             action_matches = self._matcher(sent)
    #             if action_matches:
    #                 new_header = sent
    #                 test.header.append(new_header.text)
    #     test.steps[step_index].action = nlp("".join([sent.text for sent in sents if not self._matcher(sent)]))
    #     return test