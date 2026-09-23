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

# Passende Projekt-ID ermitteln
projekt_id = projekte.loc[
    projekte["projektname"] == projekt,
    "projekt_id"
].iloc[0]


# --------------------------------------------------
# ZEITRAUM AUSWÄHLEN
# --------------------------------------------------

def load_date_range(projekt_id):
    conn = get_connection()

    query = """
        SELECT
            MIN(berichtsmonat) AS min_datum,
            MAX(berichtsmonat) AS max_datum
        FROM monatsberichte
        WHERE projekt_id = %s;
    """

    df = pd.read_sql(query, conn, params=(projekt_id,))
    conn.close()

    return df


zeitraum = load_date_range(projekt_id)

min_datum = zeitraum["min_datum"].iloc[0]
max_datum = zeitraum["max_datum"].iloc[0]

if min_datum is not None and max_datum is not None:

    col1, col2 = st.columns(2)

    with col1:
        von_datum = st.date_input(
            "Von",
            value=min_datum,
            min_value=min_datum,
            max_value=max_datum
        )

    with col2:
        bis_datum = st.date_input(
            "Bis",
            value=max_datum,
            min_value=min_datum,
            max_value=max_datum
        )

else:
    st.warning("Für dieses Projekt sind noch keine Monatsdaten vorhanden.")
