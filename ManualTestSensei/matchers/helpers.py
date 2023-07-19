from pipeline import Test, Step, Smell
import spacy

def _store_smell(container: Test|Step, smell_name:str, hint:str, where:str, term:spacy.tokens.Span) -> None:
    smell = Smell(smell_name, where, hint, term)
    container.smells.append(smell)
    return None