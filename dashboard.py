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

# --------------------------------------------------
# PROJEKTE AUS DER DATENBANK LADEN
# --------------------------------------------------

def load_projects():
    conn = get_connection()

    query = """
        SELECT DISTINCT projekt_id, projektname
        FROM monatsberichte
        ORDER BY projektname;
    """

    df = pd.read_sql(query, conn)
    conn.close()

    return df


try:
    projekte = load_projects()

    st.subheader("Projekt auswählen")

    if projekte.empty:
        st.warning("In der Datenbank wurden noch keine Projekte gefunden.")
    else:
        projekt = st.selectbox(
            "Projekt",
            projekte["projektname"].tolist()
        )

        st.success(f"Ausgewähltes Projekt: {projekt}")

except Exception as e:
    st.error("Die Daten konnten nicht aus der Datenbank geladen werden.")
    st.exception(e)
