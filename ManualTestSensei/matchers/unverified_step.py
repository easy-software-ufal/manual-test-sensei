from pipeline import Test
import smells_names

def unverified_step(test: Test):
    """
    Missing verification step
    """
    steps = test.steps
    unverified_steps = [step for step in steps if len(step.reactions) == 0]
    for step in unverified_steps:
        _store_smell(step, smells_names.UNVERIFIED_ACTION, '', 'action', step.action)
