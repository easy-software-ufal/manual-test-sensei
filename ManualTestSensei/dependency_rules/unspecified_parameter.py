from data import expand_words

unspecific_words = expand_words(('all', 'default', 'any', 'some'), k=5)

patterns = [
            {'RIGHT_ID': 'anchor','RIGHT_ATTRS': {'POS': 'NOUN'}},
            {'RIGHT_ID': 'determinant','LEFT_ID':'anchor','REL_OP':'>', 'RIGHT_ATTRS': {'LOWER': {'IN': unspecific_words}}}
        ]
