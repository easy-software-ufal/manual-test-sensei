from spacy.matcher import DependencyMatcher, Matcher
from pipeline import nlp
from dependency_rules import conditional_test, misplaced_precondition, undefined_wait, misplaced_result_verification, \
    ambiguous_test_adjectives, ambiguous_test_comparative_adverbs, ambiguous_test_adverbs_of_manner, \
    ambiguous_test_indefinite_determiners, ambiguous_test_indefinite_pronouns, misplaced_result_affirmative_sentences, \
    eager_step, misplaced_step


class MatchersFactory:

    def conditional_test_matcher():
        return MatchersFactory._build_matcher(conditional_test.patterns)

    def misplaced_precondition_matcher():
        return MatchersFactory._build_dependency_matcher(misplaced_precondition.patterns)

    def misplaced_action_matcher():
        return MatchersFactory._build_matcher(misplaced_step.patterns)

    # def undefined_wait_matcher():
    #     return MatchersFactory._build_dependency_matcher(undefined_wait.patterns)

    def misplaced_verification_matcher():
        return MatchersFactory._build_dependency_matcher(misplaced_result_verification.patterns)

    def misplaced_result_affirmative_sentences():
        return MatchersFactory._build_dependency_matcher(misplaced_result_affirmative_sentences.patterns)

    def ambiguous_test_adjectives_matcher():
        return MatchersFactory._build_matcher(ambiguous_test_adjectives.patterns)

    def ambiguous_test_comparative_adverbs_matcher():
        return MatchersFactory._build_matcher(ambiguous_test_comparative_adverbs.patterns)

    def ambiguous_test_adverbs_of_manner_matcher():
        return MatchersFactory._build_matcher(ambiguous_test_adverbs_of_manner.patterns)

    def ambiguous_test_indefinite_determiners_matcher():
        return MatchersFactory._build_matcher(ambiguous_test_indefinite_determiners.patterns)

    def ambiguous_test_indefinite_pronouns_matcher():
        return MatchersFactory._build_matcher(ambiguous_test_indefinite_pronouns.patterns)

    def eager_step_matcher():
        return MatchersFactory._build_matcher(eager_step.patterns)

    def _build_dependency_matcher(patterns):
        matcher = DependencyMatcher(nlp.vocab)
        patterns = enumerate(patterns)
        for idx, pattern in patterns:
            matcher.add('rule' + str(idx), [pattern])
        return matcher

    def _build_matcher(patterns):
        matcher = Matcher(nlp.vocab)
        patterns = enumerate(patterns)
        for idx, pattern in patterns:
            matcher.add('rule' + str(idx), [pattern])
        return matcher


if __name__ == '__main__':
    a = """
<dl>
    <dt>Go to the View menu and select Windows > Connections</dt>
        <dd>The connections Window opens</dd>
    <dt>On the Audio tab, verify that there is a capture device on the left (under System) that is connected to one of the Qtractor Master Ins on the right hand side</dt>
    <dt>Go to the Track menu and choose Add Track or use Ctrl+Shift+N</dt>
        <dd>The Track properties window opens</dd>
    <dt>On the Track tab, name the track and choose the Audio option, then click OK</dt>
        <dd>The new track appears in the Track pane</dd>
    <dt>Arm the new track for recording by clicking the R button in the track listing on the left of the Qtractor window.</dt>
    <dt>Click the Record button in the top toolbar</dt>
        <dd>The Session window opens</dd>
    <dt>Give a name for the file that will hold this recorded input and Click OK</dt>
    <dt>Click the Play button in the top toolbar and start singing/playing into the microphone/input device</dt>
        <dd>The track pan displays the recorded waveform and scrolls along</dd>
    <dt>Click the stop button when you have recorded enough</dt>
    <dt>Click the "Backward" button until the track marker returns to the start</dt>
    <dt>Click on play to hear the two track play</dt>
        <dd>The track plays through your speakers</dd>
</dl>
"""
    m = MatchersFactory.conditional_test_matcher()
    doc = nlp(a)
    r = m(doc)
    match_id, token_ids = r[0]
    for i in range(len(token_ids)):
        print(doc[token_ids[i]].text)
    print(r)
