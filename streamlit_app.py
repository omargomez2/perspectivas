
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


st.title('Estado de envíos')

ccount = run_query("SELECT count(*) from postgre_capleftus.public.perspectivas;")
st.header('Número de envíos activos '+ str(ccount[0][0]))

rows_env_delta = run_query("SELECT * from envíos_delta;")
df_env_delta = pandas.DataFrame(rows_env_delta, columns = ['Año' , 'Envíos', 'Delta'])
st.dataframe(df_env_delta, 1440, 540)

col1, col2, col3 = st.columns(3)
col1.metric("Envíos 2018", df_env_delta.at[0,"Envíos"] , df_env_delta.at[0,"Delta"])
col2.metric("Envíos 2019", df_env_delta.at[1,"Envíos"] , df_env_delta.at[1,"Delta"])
col3.metric("Envíos 2020", df_env_delta.at[2,"Envíos"] , df_env_delta.at[2,"Delta"])


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
#st.line_chart(df_envios)

conn.close()
