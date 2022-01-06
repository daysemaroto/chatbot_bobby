import stanza
import spacy
import spacy_stanza
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import stopwords

from string import punctuation
import pandas as pd
import re


dfsanos = pd.read_pickle('./sanos.pkl')
dfnosanos = pd.read_pickle('./nosanos.pkl')

df = pd.concat([dfsanos, dfnosanos])

list_alimentos = df.alimento.tolist()
list_lemmalimentos = df.lemma.tolist()


def init_stanza():
    # Download the stanza model if necessary
    nltk.download('stopwords')
    stanza.download("es")

    # Initialize the pipeline
    return spacy_stanza.load_pipeline("es")

nlp = init_stanza()

def get_stopwords():
    stops=['!','?']
    mystopwords = set(stopwords.words('spanish'))
    mystopwords |= set(mystopwords)
    return mystopwords

def tokenize(phrase):
    return [word.text.lower() for word in nlp(phrase)]

def lemmatize_with_stop(phrase):
    return [word.lemma_.lower() for word in nlp(phrase)]
    
def lemmatize_without_stop(phrase):
    return [w.lemma_ for w in nlp(phrase.lower()) if w.text not in get_stopwords()]

def remove_accent_punct(textList):
    #for removing accent and punctuation
    a,b = 'áéíóúü','aeiouu'
    trans=str.maketrans(a,b)
    remove_punct = str.maketrans('', '', punctuation)
    cleanList  = [l.translate(trans) for l in textList]
    cleanList = [l.translate(remove_punct) for l in cleanList]
    cleanList  = [text.strip().lower() for text in cleanList if text.strip()!='']
    return cleanList

def get_lemmas_from_list(textList):
    #word by word in a list
    listnlp = [lemmatize_without_stop(t) for t in textList]
    return [' '.join(remove_accent_punct(l)) for l in listnlp]
    
def get_lemmas_from_text(phrase):
    lemmas = lemmatize_without_stop(phrase)
    return remove_accent_punct(lemmas)

def clean(sentence):
    sw = lemmatize_without_stop(sentence)
    sw = remove_accent_punct(sw)
    return ' '.join(sw)

def aliment_lemma(row):
    return clean(row.alimento)

def clase_lemma(row):
    return clean(row.clase)

def final_sentence(sentence):
    clsent = clean(sentence)
    if ('frutonecer' in clsent):
        return clsent.replace('frutonecer', 'frutoseco')
    for i in range(len(list_alimentos)):
        if list_alimentos[i] in clsent:
            alimento = list_alimentos[i]
            clase =  df.query("alimento==@alimento")["clase_lemma"].iloc[0]
        elif list_lemmalimentos[i] in sentence:
            alimento = list_lemmalimentos[i]
            clase = df.query("lemma==@alimento")["clase_lemma"].iloc[0]
        else:
            clase = None
        if clase:
            clsent = clsent.replace(alimento, clase)
            break
    return clsent
