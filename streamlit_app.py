#-------------------
# Author: OG 2023
# url: https://omargomez2-perspectivas-streamlit-app-gn22jw.streamlit.app/
# Description: Perspectivas Journal Report
#------------------

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

rows_env_delta = run_query("SELECT * from envíos_delta;")
df_env_delta = pandas.DataFrame(rows_env_delta, columns = ['Año' , 'Envíos', 'Delta'])

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Envíos 2018", round(df_env_delta.loc[0].at["Envíos"]), round(df_env_delta.loc[0].at["Delta"]))
col2.metric("Envíos 2019", round(df_env_delta.loc[1].at["Envíos"]), round(df_env_delta.loc[1].at["Delta"]))
col3.metric("Envíos 2020", round(df_env_delta.loc[2].at["Envíos"]), round(df_env_delta.loc[2].at["Delta"]))
col4.metric("Envíos 2021", round(df_env_delta.loc[3].at["Envíos"]), round(df_env_delta.loc[3].at["Delta"]))
col5.metric("Envíos 2022", round(df_env_delta.loc[4].at["Envíos"]), round(df_env_delta.loc[4].at["Delta"]))
col6.metric("Envíos 2023", round(df_env_delta.loc[5].at["Envíos"]), round(df_env_delta.loc[5].at["Delta"]))

ccount = run_query("SELECT count(*) from postgre_capleftus.public.perspectivas;")
st.header('Número de envíos activos: '+ str(ccount[0][0]))

rows = run_query("SELECT paper, titulo, enviado, DATE_PART('day', CURRENT_DATE::timestamp - enviado::timestamp) as días, autores, estado, notas, monitor from postgre_capleftus.public.perspectivas;")
dfp = pandas.DataFrame(rows, columns = ['Paper Id' , 'Título' , 'Enviado' , 'Días', 'Autores' , 'Estado' , 'Notas', 'Monitor'])
dfp.Días = dfp.Días.round().astype(int)
dfp = dfp.set_index('Paper Id')

st.dataframe(dfp, 1440, 540)


rows_env = run_query("select DATE_PART('year', \"Fecha de envío\"::date) as año, count(*) as envíos from articles_rp ar group by año order by año;")
df_envios = pandas.DataFrame(rows_env, columns = ['Año' , 'Envíos'])
df_envios.Año = df_envios.Año.round().astype(int)
df_envios = df_envios.set_index('Año')

#st.dataframe(df_envios)
st.header('Número de envíos por año')
st.bar_chart(df_envios)

rows_estado = run_query("select * from estado;")
df_aux = pandas.DataFrame(rows_estado, columns = ['Año' , 'Envíos', 'En revisión','Publicados','Rechazados', 'En producción', 'Tasa'])
df_aux.Año = df_aux.Año.round().astype(int)
#df_aux = df_aux.set_index('Año')

df_estado = df_aux.drop(['En revisión','En producción','Tasa'], axis=1)
df_estado = df_estado.set_index('Año')

st.header('Estado por año')
st.bar_chart(df_estado)
#st.line_chart(df_estado)

#st.dataframe(df_aux)

col7, col8, col9, col10, col11, col12 = st.columns(6)
col7.metric("Tasa A. 2018", df_aux.loc[0].at["Tasa"], "0")
col8.metric("Tasa A. 2019", df_aux.loc[1].at["Tasa"], "0")
col9.metric("Tasa A. 2020", df_aux.loc[2].at["Tasa"], "0")
col10.metric("Tasa A. 2021", df_aux.loc[3].at["Tasa"], "0")
col11.metric("Tasa A. 2022", df_aux.loc[4].at["Tasa"], "0")
col12.metric("Tasa A. 2023", df_aux.loc[5].at["Tasa"], "0")


conn.close()