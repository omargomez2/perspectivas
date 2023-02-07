#-------------------
# Author: OG 2023
# url: https://omargomez2-perspectivas-streamlit-app-gn22jw.streamlit.app/
# Description: Perspectivas Journal Report
#-------------------

import streamlit as st
import pandas
import psycopg2
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Initialize connection.
# Uses st.experimental_singleton to only run once.
#-@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
#@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows_aux = run_query("select * from estado_d;")
rows_papers = run_query("SELECT paper, titulo, enviado, DATE_PART('day', CURRENT_DATE::timestamp - enviado::timestamp) as días, autores, estado, notas, monitor from postgre_capleftus.public.perspectivas;")

conn.close()


st.title('Revista Perspectivas')

#---- Envíos
st.header('Número de manuscritos enviados por año')
df_aux = pandas.DataFrame(rows_aux, columns = ['Año' , 'Envíos', 'En revisión','Publicados','Rechazados', 'En producción', 'Tasa', 'Delta env','Delta tasa'])

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("2018", round(df_aux.loc[0].at["Envíos"]), df_aux.loc[0].at["Delta env"])
col2.metric("2019", round(df_aux.loc[1].at["Envíos"]), round(df_aux.loc[1].at["Delta env"]))
col3.metric("2020", round(df_aux.loc[2].at["Envíos"]), round(df_aux.loc[2].at["Delta env"]))
col4.metric("2021", round(df_aux.loc[3].at["Envíos"]), round(df_aux.loc[3].at["Delta env"]))
col5.metric("2022", round(df_aux.loc[4].at["Envíos"]), round(df_aux.loc[4].at["Delta env"]))
col6.metric("2023", round(df_aux.loc[5].at["Envíos"]), round(df_aux.loc[5].at["Delta env"]))


#--- Manuscritos activos
dfp = pandas.DataFrame(rows_papers, columns = ['Paper Id' , 'Título' , 'Enviado' , 'Días', 'Autores' , 'Estado' , 'Notas', 'Monitor'])
dfp.Días = dfp.Días.round().astype(int)
dfp = dfp.set_index('Paper Id')

ccount = len(dfp.index)
st.header('Número de envíos activos: '+ str(ccount))
st.dataframe(dfp, 1440, 540)


#---- Gráfico de enviados
df_envios = df_aux.drop(['En revisión','Publicados','Rechazados', 'En producción', 'Tasa', 'Delta env','Delta tasa'], axis=1)
#df_envios.Año = df_envios.Año.round().astype(int)
df_envios = df_envios.set_index('Año')

st.header('Envíos por año')
st.bar_chart(df_envios)
#st.dataframe(df_envios)


#---Gráfico de estado
df_estado = df_aux.drop(['En revisión', 'En producción', 'Tasa', 'Delta env','Delta tasa'], axis=1)
df_estado = df_estado.set_index('Año')

st.header('Estado por año')
st.bar_chart(df_estado)
#st.line_chart(df_estado)


#---Métrica tasa de aceptación
st.header('Tasa de aceptación por año')
col7, col8, col9, col10, col11, col12 = st.columns(6)
col7.metric("2018", df_aux.loc[0].at["Tasa"], df_aux.loc[1].at["Delta tasa"])
col8.metric("2019", str(round(df_aux.loc[1].at["Tasa"]))+'%', df_aux.loc[1].at["Delta tasa"])
col9.metric("2020", str(round(df_aux.loc[2].at["Tasa"]))+'%', str(round(df_aux.loc[2].at["Delta tasa"]))+'%')
col10.metric("2021", str(round(df_aux.loc[3].at["Tasa"]))+'%', str(round(df_aux.loc[3].at["Delta tasa"]))+'%')
col11.metric("2022", str(round(df_aux.loc[4].at["Tasa"]))+'%', str(round(df_aux.loc[4].at["Delta tasa"]))+'%')
#col12.metric("Tasa A. 2023", df_aux.loc[5].at["Tasa"], "0")

res = ' '.join(dfp['Título'])
st.write(res)