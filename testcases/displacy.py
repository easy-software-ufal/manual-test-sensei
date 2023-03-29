from spacy import displacy
import spacy

text = """Does the Xubuntu offline documentation open?"""
nlp = spacy.load("en_core_web_lg")
doc = nlp(text)
displacy.serve(doc)