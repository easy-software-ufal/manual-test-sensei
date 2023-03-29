from pipeline import nlp
from spacy.matcher import DependencyMatcher
from spacy import displacy
wait_words = ('wait', 'halt', 'rest', 'holdup')
VERBS = ['VBD', 'VBG', 'VBN', 'VBZ']
if __name__ == '__main__':
    text = 'Click in the pencil of the "WebcamDisabled" A pop-up will open. Click in the Configure button. '
    doc = nlp(text)
    # displacy.serve(doc)
    matcher = DependencyMatcher(nlp.vocab)

    rule = \
            [
                {'RIGHT_ID': 'anchor','RIGHT_ATTRS': {'POS': {'IN': ['VB', 'VBP']}}},
                {'RIGHT_ID': 'second_verb','LEFT_ID':'anchor', 'RIGHT_ATTRS': {'POS': {'IN': VERBS}}, 'REL_OP': '>>'}
            ]

    matcher.add('whatever', [rule])

    print(matcher(doc))