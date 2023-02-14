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

rows_rev_act = run_query("select id, título, envío, estado, decisión, \"fecha decisión\", revisor, asignada, completado, date_part('day', current_date::timestamp-asignada::timestamp) as \"días desde asignación\" from activos_rev;")
conn.close()

#--- Manuscritos activos
#dfp = pandas.DataFrame(rows_rev_act, columns = ['Paper Id','Título','Envío','Estado','Decisión','Fecha Decisión','Revisor','F. Asignación','F. Completado','Días desde F. Asig.'])
#dfp['Días desde F. Asig.'] = dfp['Días desde F. Asig.'].round().astype(int)
#dfp = dfp.set_index('Paper Id')