import streamlit as st
import pandas as pd
import spacy
##import csv

@st.cache
def convert_df(df):
   return df.to_csv(sep=";", index=False, quoting=3).encode('utf-8') #3 = csv.QUOTE_NONE

def lemas(text, nlp):
    text = nlp(text.lower())
    lista = [token.lemma_ for token in text if token.pos_ in [u'NOUN', u'ADJ', u'PROPN', u'VERB']]
    return lista #','.join(lista)

st.title('Lematiza CSV')
st.text('Cargar archivo CSV separado con punto y coma.')
st.text('Primera Columna: ID')
st.text('Segunda Columna: Texto')

data = st.file_uploader("Cargar CSV", type=["csv"], accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False)

if data is not None:
##with open(data, newline='') as csvfile:
    ##csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    nlp = spacy.load('es_core_news_sm', disable=['ner'])
    dataframe = pd.read_csv(data, delimiter=";")
    dataframe["Lemas"] = dataframe[dataframe.columns[1]].apply(lemas, args=(nlp,))
    count = {}
    for index, value in dataframe["Lemas"].items():
        for palabra in value:
            count.setdefault(palabra, 0)
            count[palabra] = count[palabra] + 1

    ncount = sorted(
        [[k, v, i] for i, (k, v) in enumerate(count.items())], key=lambda r:r[1], reverse=True)

    st.write(ncount)
    #st.write(dataframe)
    
    st.download_button(
       "Descargar salida",
       convert_df(dataframe),
       "Salida.csv",
       "text/csv",
       key='download-csv'
    )