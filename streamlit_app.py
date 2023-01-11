
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
st.dataframe(rows)

#df=st.dataframe(rows)
#df.columns = ['col1','col2','col3','col4']

#df.rename(columns={'col1':'new_col1','col2':'new_col2','col3':'new_col3','col4':'new_col4'}, inplace = True)
#st.dataframe(df)

# Print results.
#for row in rows:
#    st.write(f"{row[0]} has a :{row[1]}:")

conn.close()
