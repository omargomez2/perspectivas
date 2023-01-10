
import streamlit as st
import pandas
import psycopg2


conn = psycopg2.connect(**st.secrets["postgres"])

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)

# Creating a cursor object using the cursor() method
cur = conn.cursor()

# Executing an MYSQL function using the execute() method
cur.execute("select version()")

# Fetch a single row using fetchone() method.
data = cur.fetchone()

st.write("Connection established to: ", data)

# Closing the connection
conn.close()

#def run_query(query):
#    with conn.cursor() as cur:
#        cur.execute(query)
#        return cur.fetchall()

#rows = run_query("SELECT * from perspectivas;")

# Print results.
##for row in rows:
##    st.write(f"{row[0]} has a :{row[1]}:")
