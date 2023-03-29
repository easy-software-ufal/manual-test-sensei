patterns = [
            [
                # anchor token: verb
                {
                    'RIGHT_ID': 'anchor',
                    'RIGHT_ATTRS': {'POS': 'VERB'}
                },
                # verb -> subject
                {
                    "LEFT_ID": "anchor",
                    "REL_OP": ">",
                    'RIGHT_ID': 'subject',
                    'RIGHT_ATTRS': {'POS': 'NOUN', 'DEP': {'IN': ['nsubj', 'nsubjpass']}}
                },
                # subject before auxiliary
                {
                    'LEFT_ID': 'subject',
                    'REL_OP': '$++',
                    'RIGHT_ID': 'auxiliary',
                    'RIGHT_ATTRS': {'POS': 'AUX', 'DEP': {'IN': ['aux', 'auxpass', 'cop']}, 'MORPH': {'IS_SUPERSET': ['Mood=Ind']}}
                }
            ]
        ]
