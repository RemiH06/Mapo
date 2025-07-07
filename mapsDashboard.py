import streamlit as st
import csv
import os
import xml.etree.ElementTree as ET
import folium
from streamlit_folium import st_folium

estados = []

# Tomamos el csv de estados y creamos el objeto estado
with open("estados.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        nombre = row["estado"]
        clave = row["clave"]
        # Cheatin'
        id_estado = clave[-2:]
        estados.append({
            "nombre": nombre,
            "id": id_estado,
            "kml": None
        })

data_packs = "data_packs"

# Buscamos los kml
for estado in estados:
    id_estado = estado["id"]
    
    if id_estado == "00": continue
    # comentamos la prueba de 14
    # if id_estado != "14": continue
    
    # ##.XYZ
    try:
        posibles_dirs = [d for d in os.listdir(data_packs) if d.startswith(id_estado)]
        if not posibles_dirs:
            print(f"No se encontró carpeta para el estado {estado['nombre']} con id {id_estado}")
            continue
        
        estado_dir = os.path.join(data_packs, posibles_dirs[0])
        
        # zc_##
        zc_folder = f"zc_{id_estado}"
        zc_path = os.path.join(estado_dir, zc_folder)
        if not os.path.isdir(zc_path):
            print(f"No se encontró carpeta {zc_folder} dentro de {estado_dir}")
            continue
        
        # kml
        kml_files = [f for f in os.listdir(zc_path) if f.endswith(".kml")]
        if not kml_files:
            print(f"No se encontró archivo .kml en {zc_path}")
            continue
        
        kml_file_path = os.path.join(zc_path, kml_files[0])
        
        with open(kml_file_path, "r", encoding="utf-8") as f:
            kml_content = f.read()
            estado["kml"] = kml_content
            
    except Exception as e:
        print(f"Error procesando estado {estado['nombre']}: {e}")

# print([estado["id"] for estado in estados])

st.title("Look mom i'm on TV :D")

# Filtros de estado en una sidebar
st.sidebar.title("Filtros de estados")
seleccionados = []
for estado in estados:
    if estado["kml"]:
        checked = st.sidebar.checkbox(estado["nombre"], value=False)
        if checked:
            seleccionados.append(estado)

# Focus de MX
m = folium.Map(location=[23.6345, -102.5528], zoom_start=5)

# Graficamos
for estado in seleccionados:
    # creds a chappy
    if estado["kml"]:
        try:
            root = ET.fromstring(estado["kml"])
            ns = {"kml": "http://www.opengis.net/kml/2.2"}

            for polygon in root.findall(".//kml:Polygon", ns):
                coords_text = polygon.find(".//kml:coordinates", ns)
                if coords_text is not None:
                    coords_pairs = coords_text.text.strip().split()
                    coords = []
                    for pair in coords_pairs:
                        lon, lat, *_ = pair.split(",")
                        coords.append([float(lat), float(lon)])
                    folium.Polygon(
                        locations=coords,
                        color="blue",
                        weight=2,
                        fill=True,
                        fill_opacity=0.3,
                        popup=estado["nombre"]
                    ).add_to(m)
        except Exception as e:
            print(f"Error graficando estado {estado['nombre']}: {e}")

st_data = st_folium(m, width=700, height=500)
