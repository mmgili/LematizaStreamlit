import streamlit as st
import pandas as pd
import spacy
##import csv

def lemas(text, nlp):
    text = nlp(text)
    lista = [token.lemma_.lower() for token in text if token.pos_ in [u'NOUN', u'ADJ', u'PROPN', u'VERB']]
    return ','.join(lista)

st.title('Lematiza CSV')

data = st.file_uploader("Cargar CSV", type=["csv"], accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False)

if data is not None:
##with open(data, newline='') as csvfile:
    ##csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    nlp = spacy.load('es_core_news_sm', disable=['ner'])
    dataframe = pd.read_csv(data, delimiter=";")
    dataframe["Lemas"] = dataframe[dataframe.columns[1]].apply(lemas, args=(nlp,))
    st.write(dataframe)
