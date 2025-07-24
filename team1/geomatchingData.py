import geopandas as gpd
import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt

# Leer las MZAs
blocks = gpd.read_file(r'team1\data\conjunto_de_datos\01m.shp')
# Leer los CPs
cps = gpd.read_file(r'team1\data\CP_01Ags_v11.shp')
# Estandarizar las CRS (Sistema de Referencia de Coordenadas) 
cps = cps.to_crs(blocks.crs)


# Calcular el área de las MZAs
blocks['area_mza'] = blocks.geometry.area
# Intersectar las MZAs y CPs en base al mayor área de pertenencia
intersected = gpd.overlay(blocks, cps, how='intersection')
intersected['area_intersect'] = intersected.geometry.area
# Porcentaje de intersección
intersected['intersect_percent'] = intersected['area_intersect'] / intersected['area_mza']
# Matchear en base al mayor porcentaje de pertenencia
match = (intersected.sort_values('intersect_percent', ascending=False)
         .drop_duplicates(subset='CVEGEO'))
match = match.rename(columns={'d_codigo': 'CP'})

# Output
blocks_matched = blocks.merge(
    match[['CVEGEO', 'intersect_percent', 'CP']], 
    on='CVEGEO', 
    how='left'
    )

display(blocks_matched.head())
# Dfs Shapes
print(f'Input: {blocks.shape}')
print(f'Output: {blocks_matched.shape}')

bad_matches = blocks_matched[blocks_matched['intersect_percent'] < 0.75]
print(f'Matcheos imperfectos: {bad_matches.shape[0]}')

