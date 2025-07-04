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

indicador_df = pd.read_csv("indicadores.csv", encoding="utf-8")

# Funciones de filtrado
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
        "subclases5": df["Subclase5"].dropna().unique(),
        "indicadores": dict(zip(df["Nombre"], df["ID"]))
    }

# Interfaz Streamlit
st.title("Dashboard INEGI - Indicador Ejemplo")

estado = st.selectbox("Selecciona un estado:", options=list(estado_claves.keys()))
recientes = st.checkbox("Mostrar datos recientes", value=False)
bdi = st.selectbox("Selecciona BDI:", options=["BIE", "BISE"])

# filtros dinámicos
filters = get_filters(bdi)
sect = st.selectbox("Selecciona un sector:", options=filters["sects"])
filters = get_filters(bdi, sect)
clase = st.selectbox("Selecciona una clase:", options=filters["clases"])
filters = get_filters(bdi, sect, clase)
subclase = st.selectbox("Selecciona una subclase:", options=filters["subclases"])
filters = get_filters(bdi, sect, clase, subclase)
subclase2 = st.selectbox("Selecciona segunda subclase:", options=filters["subclases2"])
filters = get_filters(bdi, sect, clase, subclase, subclase2)
subclase3 = st.selectbox("Selecciona tercera subclase:", options=filters["subclases3"])
filters = get_filters(bdi, sect, clase, subclase, subclase2, subclase3)
subclase4 = st.selectbox("Selecciona cuarta subclase:", options=filters["subclases4"])
filters = get_filters(bdi, sect, clase, subclase, subclase2, subclase3, subclase4)
subclase5 = st.selectbox("Selecciona quinta subclase:", options=filters["subclases5"])

# indicadores filtrados finales
filters = get_filters(bdi, sect, clase, subclase, subclase2, subclase3, subclase4, subclase5)
indicadores_filtrados = filters["indicadores"]

if indicadores_filtrados:
    indicador_id = st.selectbox("Selecciona un indicador:", options=list(indicadores_filtrados.keys()))
else:
    st.warning("No hay indicadores que coincidan con los filtros seleccionados.")
    st.stop()

# Construcción URL
token = get_token()
url = (
    f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/"
    f"{indicadores_filtrados[indicador_id]}/es/0{estado_claves[estado]}/{str(recientes).lower()}/"
    f"{bdi}/2.0/{token}?type=json"
)

st.text(f"Consulta generada: {url}")

# Obtener datos
res = requests.get(url)
if res.status_code != 200:
    st.error(f"Error al obtener datos del INEGI: {res.status_code}")
else:
    try:
        content = res.json()
        series = content.get("Series", [])
        if series and isinstance(series, list):
            observations = series[0].get("OBSERVATIONS", [])
        else:
            observations = []
    except Exception as e:
        st.error(f"No se pudo procesar la respuesta: {e}")
        observations = []

    if observations:
        df = pd.DataFrame(observations)
        st.dataframe(df)

        csv = df.to_csv(index=False, encoding="utf-8")
        st.download_button(
            label="Descargar datos como CSV",
            data=csv,
            file_name="observaciones.csv",
            mime="text/csv"
        )
    else:
        st.write("No se encontraron observaciones")

# Mostrar resumen de filtros
st.text("Consultas posibles con los filtros elegidos:")
st.text(f"BDI: {bdi}, Sector: {sect}, Clase: {clase}, Subclase: {subclase}, Subclase2: {subclase2}, "
        f"Subclase3: {subclase3}, Subclase4: {subclase4}, Subclase5: {subclase5}")
