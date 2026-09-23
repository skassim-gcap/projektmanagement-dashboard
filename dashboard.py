import streamlit as st
import psycopg2
import pandas as pd


# --------------------------------------------------
# SEITENEINSTELLUNGEN
# --------------------------------------------------

st.set_page_config(
    page_title="Projektmanagement Dashboard",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# DATENBANKVERBINDUNG
# --------------------------------------------------

def get_connection():
    database_url = st.secrets["DATABASE_URL"]
    return psycopg2.connect(database_url)


# --------------------------------------------------
# TITEL
# --------------------------------------------------

st.title("PROJEKTMANAGEMENT DASHBOARD")
st.write("Auswertung der monatlichen Projektdaten")
