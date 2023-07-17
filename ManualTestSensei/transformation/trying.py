import spacy
import ast
nlp = spacy.load("en_core_web_sm")

#terms = "['Click', 'and Reboot', ', Retry']"
terms = "['Log', ', shutdown', 'or restart']"
terms = ast.literal_eval(terms)
terms = terms[1:]

print(terms)

for index, item in enumerate(terms):
    doc = nlp(item)
    if doc[0].pos_ == 'CCONJ' or doc[0].text == ',':
        sentence = item.split()
        sentence = ' '.join(sentence[1:])
        terms[index] = sentence


print(terms)
sentence = '<dt> Log out, shutdown or restart</dt'
#sentence = "<dt> Click on the Website and Reboot the system, Retry if error </dt>"
#sentence = "<dt> This will be alright so Click on the Website and Reboot the system </dt>"
output = sentence
for term in terms:
    output = output.replace(term, "</dt> <dt> " + term + ' ')

print(output)

import re

output = '<dt>Log out, </dt>\n\t <dt> shutdown or </dt>\n\t <dt> restart</dt>'

# Extrair o conteúdo entre as tags <dt> e </dt> e realizar o strip
pattern = r"<dt>(.*?)</dt>"
result = [item.strip() for item in re.findall(pattern, output)]

print(result)

new_result = []

for item in result:
    doc = nlp(item)

    print(doc[-1])
    if doc[-1].pos_ == 'CCONJ' or doc[-1].text == ',':
        new_result.append(doc[:-1])
        #print(doc[:-1])
    else:
        new_result.append(doc)
    # if tokens and (tokens[-1] == ',' or tokens[-1].pos_ == 'CCONJ'):
    #     new_result.append(' '.join(tokens[:-1]))
    # else:
    #     new_result.append(item)

print(new_result)
output = ""
for element in new_result:
    output += "<dt>" + str(element) + "</dt>\n\t"
print(output)