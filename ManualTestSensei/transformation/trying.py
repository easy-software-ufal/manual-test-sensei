import spacy
import ast
nlp = spacy.load("en_core_web_sm")

terms = "['Click', 'and Reboot', ', Retry']"
lista = ast.literal_eval(terms)
lista = lista[1:]

print(lista)

for index, item in enumerate(lista):
    doc = nlp(item)
    if doc[0].pos_ == 'CCONJ' or doc[0].text == ',':
        sentence = item.split()
        sentence = ' '.join(sentence[1:])
        lista[index] = sentence


print(lista)
sentence = "<dt> Click on the Website and Reboot the system, Retry if error </dt>"
#sentence = "<dt> This will be alright so Click on the Website and Reboot the system </dt>"
output = sentence
for term in lista:
    output = output.replace(term, "</dt> <dt> " + term)

print(output)
