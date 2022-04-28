import streamlit as st
import pandas as pd
import spacy
##import csv

@st.cache
def convert_df(df):
   return df.to_csv(sep=";", index=False, quoting=3).encode('utf-8') #3 = csv.QUOTE_NONE

def lemas(text, nlp, lista_pos):
    text = nlp(text.lower())
    lista = [token.lemma_ for token in text if token.pos_ in lista_pos]
    return lista #','.join(lista)

st.title('Contar palabras')
st.text('Cargar archivo CSV separado con punto y coma.')
st.text('Primera Columna: ID')
st.text('Segunda Columna: Texto')

C_NOUN = st.checkbox('Sustantivos comunes', value=True)
C_PROPN = st.checkbox('Sustantivos propios', value=True)
C_ADJ = st.checkbox('Adjetivos', value=True)
C_VERB = st.checkbox('Verbos', value=True)
C_ADV = st.checkbox('Adverbios', value=True)
cant_palabras = st.number_input('Cantidad de palabras', min_value=1, value=50)

lista_pos = []
if C_NOUN:
    lista_pos.append(u'NOUN')
if C_PROPN:
    lista_pos.append(u'PROPN')
if C_ADJ:
    lista_pos.append(u'ADJ')
if C_ADV:
    lista_pos.append(u'ADV')
if C_VERB:
    lista_pos.append(u'VERB')

data = st.file_uploader("Cargar CSV", type=["csv"], accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False)

if data is not None:
##with open(data, newline='') as csvfile:
    ##csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    nlp = spacy.load('es_core_news_sm', disable=['ner'])
    dataframe = pd.read_csv(data, delimiter=";")
    dataframe["Lemas"] = dataframe[dataframe.columns[1]].apply(lemas, args=(nlp, lista_pos,))
    count = {}
    for index, value in dataframe["Lemas"].items():
        for palabra in value:
            count.setdefault(palabra, 0)
            count[palabra] = count[palabra] + 1

    ncount = sorted(
        [[k, v] for k, v in count.items()], key=lambda r:r[1], reverse=True)

    for palabra in ncount[:cant_palabras]:
        for index, value in dataframe["Lemas"].items():
            if palabra[0] in value:
                dataframe.at[index, palabra[0]] = '1'

    pd_ncount = pd.DataFrame(ncount)
    st.write(pd_ncount)
    st.download_button(
       "Descargar conteo",
       convert_df(pd_ncount),
       "Conteo.csv",
       "text/csv",
       key='download-csv'
    )

    st.write(dataframe)
    st.download_button(
       "Descargar salida",
       convert_df(dataframe.drop(['Lemas'], axis=1)),
       "Salida.csv",
       "text/csv",
       key='download-csv'
    )