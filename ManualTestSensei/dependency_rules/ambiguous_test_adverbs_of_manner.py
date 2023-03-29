from keywords import Keywords

adverbs_of_manner_termination = Keywords().keywords['adverbs_of_manner_termination']

patterns = [
            [
                {
                    'POS': 'ADV',
                    'TAG': 'RB',
                    'LOWER': {'REGEX': '.*' + adverbs_of_manner_termination},
                }
            ]
        ]
