

with open('arquivo_de_texto.txt', 'r+') as file:
    contents = file.read()
    article = 'any'
    index_word = 0
    pos = contents.find(article, index_word)
    contents = contents[:pos] + 'the' + contents[pos + len(article):]

    word = 'elbow'
    posicao = contents.find(word, 0)

    nova_string = word + " (1)"

    # Substitua a ocorrência encontrada pela nova string
    contents = contents[:posicao] + nova_string + contents[posicao + len(word):]
    file.seek(0)
    file.write(contents)
    file.truncate()
# # Abra o arquivo para leitura
# with open('arquivo_de_texto.txt', 'r') as arquivo:
#     # Leia o conteúdo do arquivo
#     conteudo = arquivo.read()

# # Sentença a ser procurada
# terms = 'See any'


# posicao = conteudo.find(terms)

# # Encontre o índice da primeira palavra após a sentença
# posicao_palavra = posicao + len(terms) + 1

# # Encontre a primeira palavra após a sentença
# palavra = ''
# while posicao_palavra < len(conteudo) and conteudo[posicao_palavra] != ' ':
#     palavra += conteudo[posicao_palavra]
#     posicao_palavra += 1

# # Concatene a sentença com a primeira palavra
# resultado = f'{terms} {palavra}'

# # Imprima o resultado
# print(resultado)


import spacy
# import ast
# nlp = spacy.load("en_core_web_sm")

# # text = 'See any elbow'
# terms = 'Watch it properly'
# # Esses são os terms. Preciso adicionar mais uma palavra a ele. De acordo com o texto original.

# # print(terms)
# doc = nlp(terms)
# # print(doc)

# for item in doc:
#     print(item.pos_)
#     print(type(item.pos_))
 #for index, item in enumerate(terms):

#     print(doc.pos_, doc)
#     if doc[0].pos_ == 'CCONJ' or doc[0].text == ',':
#         print(doc[0].text)
        # sentence = item.split()
        # sentence = ' '.join(sentence[1:])
        # terms[index] = sentence