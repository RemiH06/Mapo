import geopandas as gpd
import pandas as pd
from IPython.display import display

ageb_urb = gpd.read_file(r'team1\data\conjunto_de_datos\01a.shp')
ageb_rul = gpd.read_file(r'team1\data\conjunto_de_datos\01ar.shp')
# Añadir la columna faltante a las AGEBs rurales
ageb_rul['CVE_LOC'] = None
# Reordenar las columnas
ageb_rul = ageb_rul[ageb_urb.columns]
# Estandarizar los sistemas de referencia de coordenadas (CRS)
ageb_rul = ageb_rul.to_crs(ageb_urb.crs)
# Concatenar los AGEBs
agebs = gpd.GeoDataFrame(pd.concat([ageb_urb, ageb_rul], ignore_index=True), crs=ageb_urb.crs)


# Leer los CPs
cps = gpd.read_file(r'team1\data\CP_01Ags_v11.shp')
# Estandarizar las CRS 
cps = cps.to_crs(agebs.crs)


# Calcular el área de los AGEBs
agebs['area_ageb'] = agebs.geometry.area
# Intersectar las AGEBs y CPs en base al mayor área de pertenencia
intersected = gpd.overlay(agebs, cps, how='intersection')
intersected['area_intersect'] = intersected.geometry.area
# Porcentaje de intersección
intersected['intersect_percent'] = intersected['area_intersect'] / intersected['area_ageb']
# Matchear en base al mayor porcentaje de pertenencia
match = (intersected.sort_values('intersect_percent', ascending=False)
         .drop_duplicates(subset='CVE_AGEB'))

display(match.tail(20))