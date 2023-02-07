#-------------------
# Author: OG 2023
# url: https://omargomez2-perspectivas-streamlit-app-gn22jw.streamlit.app/
# Description: Perspectivas Journal Report
#-------------------

import streamlit as st
import pandas
import psycopg2

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


st.title('Revista Perspectivas')

rows_aux = run_query("select * from estado_d;")
df_auxx = pandas.DataFrame(rows_aux, columns = ['Año' , 'Envíos', 'En revisión','Publicados','Rechazados', 'En producción', 'Tasa', 'Delta env','Delta tasa'])

#---- Envíos
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Envíos 2018", round(df_auxx.loc[0].at["Envíos"]), df_auxx.loc[0].at["Delta env"])
col2.metric("Envíos 2019", round(df_auxx.loc[1].at["Envíos"]), round(df_auxx.loc[1].at["Delta env"]))
col3.metric("Envíos 2020", round(df_auxx.loc[2].at["Envíos"]), round(df_auxx.loc[2].at["Delta env"]))
col4.metric("Envíos 2021", round(df_auxx.loc[3].at["Envíos"]), round(df_auxx.loc[3].at["Delta env"]))
col5.metric("Envíos 2022", round(df_auxx.loc[4].at["Envíos"]), round(df_auxx.loc[4].at["Delta env"]))
col6.metric("Envíos 2023", round(df_auxx.loc[5].at["Envíos"]), round(df_auxx.loc[5].at["Delta env"]))


#--- Manuscritos activos
rows_papers = run_query("SELECT paper, titulo, enviado, DATE_PART('day', CURRENT_DATE::timestamp - enviado::timestamp) as días, autores, estado, notas, monitor from postgre_capleftus.public.perspectivas;")
dfp = pandas.DataFrame(rows_papers, columns = ['Paper Id' , 'Título' , 'Enviado' , 'Días', 'Autores' , 'Estado' , 'Notas', 'Monitor'])
dfp.Días = dfp.Días.round().astype(int)
dfp = dfp.set_index('Paper Id')

ccount = len(dfp.index)
st.header('Número de envíos activos: '+ str(ccount))
st.dataframe(dfp, 1440, 540)



#---- Gráfico de enviados
df_envios = df_auxx.drop(['En revisión','Publicados','Rechazados', 'En producción', 'Tasa', 'Delta env','Delta tasa'], axis=1)
#df_envios.Año = df_envios.Año.round().astype(int)
df_envios = df_envios.set_index('Año')

st.header('Envíos por año')
st.bar_chart(df_envios)
#st.dataframe(df_envios)


#---Gráfico de estado
df_estado = df_auxx.drop(['En revisión', 'En producción', 'Tasa', 'Delta env','Delta tasa'], axis=1)
df_estado = df_estado.set_index('Año')

st.header('Estado por año')
st.bar_chart(df_estado)
#st.line_chart(df_estado)



st.header('Tasa de aceptación por año')
col7, col8, col9, col10, col11, col12 = st.columns(6)
#col7.metric("Tasa A. 2018", df_aux.loc[0].at["Tasa"], "0")
col8.metric("2019", str(round(df_auxx.loc[1].at["Tasa"]))+'%', df_auxx.loc[1].at["Delta tasa"])
col9.metric("2020", str(round(df_auxx.loc[2].at["Tasa"]))+'%', str(round(df_auxx.loc[2].at["Delta tasa"]))+'%')
col10.metric("2021", str(round(df_auxx.loc[3].at["Tasa"]))+'%', str(round(df_auxx.loc[3].at["Delta tasa"]))+'%')
col11.metric("2022", str(round(df_auxx.loc[4].at["Tasa"]))+'%', str(round(df_auxx.loc[4].at["Delta tasa"]))+'%')
#col12.metric("Tasa A. 2023", df_aux.loc[5].at["Tasa"], "0")


conn.close()