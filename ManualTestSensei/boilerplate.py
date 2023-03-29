import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_lg')

text = """
    Press the ''Super Windows key'', or click the Ubuntu logo in the upper left hand unity panel and search '''Sound Recorder'''
"""
doc = nlp(text)

for sentence in doc.sents:
    print(sentence.tag_)
    #displacy.serve(sentence)
    if sentence.tag_ in ['VB', 'VBP']:
        print(True)
    print(False)