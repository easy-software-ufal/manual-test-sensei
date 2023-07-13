import spacy

# Carregar o modelo de idioma em inglês
nlp = spacy.load('en_core_web_sm')

# Função para remover as conjunções no final de uma string
def remover_conjuncoes_final(texto):
    doc = nlp(texto)
    tokens_sem_conjuncoes_final = list(doc)
    for i in reversed(range(len(doc))):
        if doc[i].pos_ == 'CCONJ':
            tokens_sem_conjuncoes_final = list(doc)[:i]
            break
    texto_sem_conjuncoes_final = ' '.join(token.text for token in tokens_sem_conjuncoes_final)
    return texto_sem_conjuncoes_final

# Lista original
lista = ["Open the door and", "try once more"]

# Remover as conjunções no final de cada string da lista
lista_sem_conjuncoes_final = [remover_conjuncoes_final(texto) for texto in lista]

print(lista_sem_conjuncoes_final)
