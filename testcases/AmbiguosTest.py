import spacy
from spacy.matcher import Matcher
from spacy import displacy

nlp = spacy.load('en_core_web_lg')
# nlp = spacy.load('pt_core_news_lg')
doc = nlp("I just saw the most popular movie of the year. The heart pumps blood around the body. John is the best at piano. We are going to the ballgame tonight. We didn\'t like the dinner. The North is cooler than the South. Look to the north and you will see the lake. I would like to swim in the Red Sea, and you?")

print(f"{'text':{12}} {'POS':{6}} {'TAG':{6}} {'Dep':{10}} {'POS explained':{20}} {'tag explained':{50}} {'Morphology'}")

for token in doc:
    if str(token.pos_) == 'DET':
        print(f'{token.text:{12}} {token.pos_:{6}} {token.tag_:{6}} {token.dep_:{10}} {spacy.explain(token.pos_):{20}} {spacy.explain(token.tag_):{50}} {token.morph}')

print("\nPattern search: ")

matcher = Matcher(nlp.vocab)
matcher.add("Ambiguous Test (verb + indefinite determiner):", [[{'POS': 'VERB'}, {'POS': 'DET','MORPH': {'NOT_IN':['Definite=Def|PronType=Art']}}]])
# matcher.add("Ambiguous Test (verb + determiner):", [[{'POS': 'VERB'}, {'POS': 'DET'}]])
# matcher.add("Ambiguous Test (determiner):", [[{'POS': 'DET'}]])
# matcher.add("Ambiguous Test (indefinite determiner):", [[{'POS': 'DET', 'MORPH': {'NOT_IN':['Definite=Def']} }]])
# # matcher.add("Ambiguous Test (indefinite):", [[{'MORPH': {'NOT_IN':['Definite=Def']}}]])
# matcher.add("Ambiguous Test (verb + indefinite determiner + !SUBSET):", [[{'POS': 'VERB'}, {'POS': 'DET','MORPH': {'IS_SUPERSET':['Definite=Def']}, 'OP': '!'}]])





matches = matcher(doc)

for match_id, start, end in matches:
    string_id = nlp.vocab.strings[match_id]  # Matcher name
    span = doc[start:end]  # The matched span of tokens
    # if "Definite=Def" not in str(span[1].morph): # spaCy knows when a determiner is definite, which we don't want
    print(string_id, span.text)
    #displacy.serve(doc)

matcher = Matcher(nlp.vocab)
matcher.add("Ambiguous Test (comparative or superlative adjectives):", [[{'TAG': {'IN': ['JJR', 'JJS']}}]])
matcher.add("Ambiguous Test (comparative or adverbs of manner):", [[{'TAG': {'IN': ['RBR', 'RB']}}]])
matches = matcher(doc)

for match_id, start, end in matches:
    string_id = nlp.vocab.strings[match_id]
    span = doc[start:end]
    print(string_id, span.text)