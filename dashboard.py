import streamlit as st
import pandas as pd
import requests
import json
from urllib.parse import quote

# Leer token desde .secrets
def get_token():
    with open(".secrets") as f:
        secrets = json.load(f)
    return secrets["token"]

# Carga de datos iniciales
estado_df = pd.read_csv("estados.csv")
estado_claves = dict(zip(estado_df["estado"], estado_df["clave"]))
indicador_df = pd.read_csv("indicadores.csv", encoding="ISO-8859-1")
indicador_ids = dict(zip(indicador_df["Nombre"], indicador_df["ID"]))

def get_filters(bdi, sect=None, clase=None, subclase=None, subclase2=None, subclase3=None, subclase4=None, subclase5=None):
    df = indicador_df[indicador_df["BDI"] == bdi]
    if sect:
        df = df[df["Sector"] == sect]
    if clase:
        df = df[df["Clase"] == clase]
    if subclase:
        df = df[df["Subclase"] == subclase]
    if subclase2:
        df = df[df["Subclase2"] == subclase2]
    if subclase3:
        df = df[df["Subclase3"] == subclase3]
    if subclase4:
        df = df[df["Subclase4"] == subclase4]
    if subclase5:
        df = df[df["Subclase5"] == subclase5]
    return {
        "sects": df["Sector"].dropna().unique(),
        "clases": df["Clase"].dropna().unique(),
        "subclases": df["Subclase"].dropna().unique(),
        "subclases2": df["Subclase2"].dropna().unique(),
        "subclases3": df["Subclase3"].dropna().unique(),
        "subclases4": df["Subclase4"].dropna().unique(),
        "subclases5": df["Subclase5"].dropna().unique()
    }

# Interfaz Streamlit
st.title("Dashboard INEGI - Indicador Ejemplo")
indicador_id = st.selectbox("Selecciona un indicador:", options=list(indicador_ids.keys()))
estado = st.selectbox("Selecciona un estado:", options=list(estado_claves.keys()))
recientes = st.checkbox("Mostrar datos recientes", value=False)
usar_bie = st.checkbox("Usar BIE en lugar de BISE", value=False)
bdi = st.selectbox("Selecciona BDI:", options=["BIE", "BISE"])

# Filtros dinámicos
filters = get_filters(bdi)
sect = st.selectbox("Selecciona un sector:", options=filters["sects"])
clase = st.selectbox("Selecciona una clase:", options=get_filters(bdi, sect)["clases"])
subclase = st.selectbox("Selecciona una subclase:", options=get_filters(bdi, sect, clase)["subclases"])
subclase2 = st.selectbox("Selecciona segunda subclase:", options=get_filters(bdi, sect, clase, subclase)["subclases2"])
subclase3 = st.selectbox("Selecciona tercera subclase:", options=get_filters(bdi, sect, clase, subclase, subclase2)["subclases3"])
subclase4 = st.selectbox("Selecciona cuarta subclase:", options=get_filters(bdi, sect, clase, subclase, subclase2, subclase3)["subclases4"])
subclase5 = st.selectbox("Selecciona quinta subclase:", options=get_filters(bdi, sect, clase, subclase, subclase2, subclase3, subclase4)["subclases5"])

token = get_token()
url = f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/{indicador_ids[indicador_id]}/es/{estado_claves[estado]}/{str(recientes).lower()}/{ 'BIE' if usar_bie else 'BISE'}/2.0/{token}?type=json"
res = requests.get(url)
if res.status_code != 200:
    st.error(f"Error al obtener datos del INEGI: {res.status_code}")
else:
    content = res.json()
    observations = content.get("Series", {}).get("OBSERVATIONS", [])
    if observations:
        df = pd.DataFrame(observations)
        st.dataframe(df)
    else:
        st.write("No se encontraron observaciones")

st.text("Consultas posibles con los filtros elegidos:")
st.text(f"BDI: {bdi}, Sector: {sect}, Clase: {clase}, Subclase: {subclase}, Subclase2: {subclase2}, Subclase3: {subclase3}, Subclase4: {subclase4}, Subclase5: {subclase5}")
