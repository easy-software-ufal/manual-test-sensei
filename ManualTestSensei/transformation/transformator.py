from pipeline import Test, Step, nlp

def unverified_action(step:Step) -> Step:
    step.reactions = list()
    step.reactions.append(nlp('[FILL_VERIFICATION]'))
    return step