from pipeline import Test, nlp
import smells_names


class UnverifiedAction:
    smell:str = smells_names.UNVERIFIED_ACTION

    def __call__(self, test: Test) -> list[Test]:
        '''Missing verification step'''
        for step in test.steps:
            if len(step.reactions) == 0:
                if len(step.action) == 0:
                    continue
                step.reactions = [nlp('[FILL_VERIFICATION]'), ]
                step.smells.append(self.smell)
        return [test, ]