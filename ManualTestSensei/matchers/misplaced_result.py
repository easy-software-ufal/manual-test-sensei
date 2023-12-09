from pipeline import Test, Step, nlp, Smell
import smells_names
from matchers import helpers
from spacy.tokens import Doc
from matchers_factory import MatchersFactory

class MisplacedResult:
    smell = smells_names.MISPLACED_RESULT

    def __call__(self, test: Test) -> list[Test]:
        '''
        A verification verb (check, verify, observe, recheck) in the step description
        Interrogative sentences as steps
        SUT state declaration after any action
        '''
        # matcher = self.is_interrogative_sentence

        test = self._apply_verification_matcher(test)
        test = self._apply_affirmative_sentence_matcher(test)
        return [test, ]

    def _apply_affirmative_sentence_matcher(self, test:Test) -> Test:
        matcher = MatchersFactory.misplaced_result_affirmative_sentences()
        for (step_index, st) in enumerate(test.steps):
            if step_index == 0:
                continue
            sentences = [sent for sent in st.action.sents]
            keep_sentences = list()
            for sent in sentences:
                matches = matcher(sent)
                if matches:
                    previous_valid_step = self.find_previous_valid_step(test, step_index)
                    test.steps[previous_valid_step].reactions.append(nlp(sent.text))
                else:
                    keep_sentences.append(sent)
            if keep_sentences:
                new_action = nlp('. '.join([sent.text for sent in keep_sentences]))
                test.steps[step_index].action = new_action
        return test

    def _apply_verification_matcher(self, test:Test) -> Test:
        matcher = MatchersFactory.misplaced_verification_matcher()
        for (step_index, st) in enumerate(test.steps):
            if step_index == 0:
                continue
            matches = matcher(st.action)
            if matches:
                step_text = st.action.text+' '+'.\n'.join([reaction.text for reaction in st.reactions])
                previous_valid_step = self.find_previous_valid_step(test, step_index)
                test.steps[previous_valid_step].reactions.append(nlp(step_text))
                test.steps[step_index] = None
        test.steps = [st for st in test.steps if st is not None]
        return test

    def find_previous_valid_step(self, test:Test, current_step:int) -> int:
            if current_step == 0:
                return 0
            if test.steps[current_step-1]:
                return current_step-1
            return self.find_previous_valid_step(test, current_step-1)