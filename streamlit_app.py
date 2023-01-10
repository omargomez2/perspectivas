
import streamlit as st
import pandas
import psycopg2


@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()



# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)

# Creating a cursor object using the cursor() method

cursor = conn.cursor()

# Executing an MYSQL function using the execute() method

cursor.execute("select version()")

# Fetch a single row using fetchone() method.

data = cursor.fetchone()

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
