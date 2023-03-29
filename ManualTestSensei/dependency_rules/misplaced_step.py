from keywords import Keywords

verifications = Keywords().keywords['verifications']

patterns = [
            [
                {
                    'POS': 'VERB',
                    'MORPH': {'IS_SUPERSET': ['VerbForm=Inf']},
                    'IS_SENT_START': True,
                    'LOWER': {'NOT_IN': verifications}
                }
            ]
        ]
