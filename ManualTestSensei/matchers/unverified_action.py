from pipeline import Test, nlp
import smells_names


class UnverifiedAction:
    smell:str = smells_names.UNVERIFIED_ACTION

    def __call__(self, test: Test) -> list[Test]:
        '''Missing verification step'''
        for step in test.steps:
            if len(step.reactions) == 0:
                step.reactions = [nlp('[Fill the verification]'), ]
                step.smells.append(self.smell)
        return [test, ]