from keywords import Keywords

verifications = Keywords().keywords['verifications']

patterns = [
            [
                {'RIGHT_ID': 'anchor', 'RIGHT_ATTRS': {'LOWER': {'IN': verifications}}}
            ]
        ]
