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
        # matcher = MatchersFactory.misplaced_result_affirmative_sentences()

        test = self._apply_verification_matcher(test)
        return [test, ]

    def _apply_verification_matcher(self, test:Test) -> Test:
        matcher = MatchersFactory.misplaced_verification_matcher()
        for (step_index, st) in enumerate(test.steps):
            if step_index == 0:
                continue
            matches = matcher(st.action)
            if matches:
                step_text = st.action.text+' '+'.\n'.join([reaction.text for reaction in st.reactions])
                test.steps[step_index-1].reactions.append(nlp(step_text))
                test.steps[step_index] = None
        test.steps = [st for st in test.steps if st is not None]
        return test

        # for st in test.steps:
        #     # First test: A verification verb in the step description
        #     action_matches = matcher(st.action)
        #     for match_id, token_ids in action_matches:
        #         for token_id in token_ids:
        #             helpers._store_smell(st, self.smell, 'verification performed', 'action', st.action[token_id])

        #     # Second test: Interrogative sentences as step
        #     for sentence in st.action.sents:
        #         if is_interrogative_sentence(sentence):
        #             helpers._store_smell(st, self.smell, 'question as step', 'action', sentence)

        # # Third test: SUT state declaration after any action
        # matcher = MatchersFactory.misplaced_result_affirmative_sentences()
        # for st in test.steps[1:]:
        #     for sentence in st.action.sents:
        #         if not (is_interrogative_sentence(sentence) or is_imperative_sentence(sentence)):
        #             action_matches = matcher(sentence)
        #             for match_id, token_ids in action_matches:
        #                 words = [sentence[token_id] for token_id in sorted(token_ids)]
        #                 helpers._store_smell(st, self.smell, 'SUT state declaration', 'action', sentence)

    def get_root(self, doc: Doc) -> list:
        return [token for token in doc if token.dep_ == 'ROOT']

    def is_imperative_sentence(self, sent: Doc) -> bool:
        root = get_root(sent)
        if root and root[0].pos_ == 'VERB' and 'VerbForm=Inf' in str(root[0].morph):
            return True
        else:
            return False

    def is_interrogative_sentence(self, sent: Doc) -> bool:
        return sent[-1].text == '?'
