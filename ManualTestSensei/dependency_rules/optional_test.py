#https://github.com/explosion/spaCy/discussions/2767


#DEPRECATED
from data import expand_words

optional_like = expand_words(('optional'),k=1)

patterns = [
            [
                {'RIGHT_ID': 'anchor','RIGHT_ATTRS': {'LOWER' : {'IN': optional_like}}}
            ]
        ]