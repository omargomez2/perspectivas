
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
#-@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from postgre_capleftus.public.perspectivas;")
#st.dataframe(rows)

dfp = pandas.DataFrame(rows, columns = ['Id', 'Título', 'Autores','Estado'])
st.dataframe(dfp)


conn.close()
