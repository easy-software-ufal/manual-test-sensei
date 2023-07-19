from pipeline import Test
import smells_names
from matchers import helpers

def find_misplaced_result(test: Test):
    """
    A verification verb (check, verify, observe, recheck) in the step description
    Interrogative sentences as steps
    SUT state declaration after any action
    """

    def get_root(doc: Doc) -> list:
        return [token for token in doc if token.dep_ == 'ROOT']

    def is_imperative_sentence(sent: Doc) -> bool:
        root = get_root(sent)
        if root and root[0].pos_ == 'VERB' and 'VerbForm=Inf' in str(root[0].morph):
            return True
        else:
            return False

    def is_interrogative_sentence(sent: Doc) -> bool:
        return sent[-1].text == '?'

    matcher = MatchersFactory.misplaced_result_verification_matcher()
    for step in test.steps:
        # First test: A verification verb in the step description
        action_matches = matcher(step.action)
        for match_id, token_ids in action_matches:
            for token_id in token_ids:
                helpers._store_smell(step, smells_names.MISPLACED_VERIFICATION, 'verification performed', 'action', step.action[token_id])

        # Second test: Interrogative sentences as step
        for sentence in step.action.sents:
            if is_interrogative_sentence(sentence):
                helpers._store_smell(step, smells_names.MISPLACED_VERIFICATION, 'question as step', 'action', sentence)

    # Third test: SUT state declaration after any action
    matcher = MatchersFactory.misplaced_result_affirmative_sentences()
    for step in test.steps[1:]:
        for sentence in step.action.sents:
            if not (is_interrogative_sentence(sentence) or is_imperative_sentence(sentence)):
                action_matches = matcher(sentence)
                for match_id, token_ids in action_matches:
                    words = [sentence[token_id] for token_id in sorted(token_ids)]
                    helpers._store_smell(step, smells_names.MISPLACED_VERIFICATION, 'SUT state declaration', 'action', sentence)
