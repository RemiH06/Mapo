import csv
import os
import time
import pandas as pd
from playwright.sync_api import sync_playwright

file_name = "indicadores_rd.csv"
proc_file = "indicadores_pd.csv"
final_file = "indicadores.csv"
def main(sector):
    
    sectores = {
        1: "Demografía y Sociedad",
        2: "Economía y Sectores Productivos",
        3: "Geografía y Medio Ambiente",
        4: "Gobierno, Seguridad y Justicia",
        5: "Indicadores económicos de coyuntura",
        6: "Ocupación, empleo y remuneraciones",
        7: "Indicadores de productividad. Base 2018",
        8: "Cuentas nacionales",
        9: "Minería",
        10: "Manufacturas",
        11: "Encuesta Nacional de Empresas Constructoras (ENEC). Serie 2018",
        12: "Encuesta Anual de Empresas Constructoras (EAEC). Serie 2018",
        13: "Encuesta mensual sobre empresas comerciales (EMEC), Base 2018",
        14: "Encuesta mensual de servicios (EMS). Serie 2018",
        15: "Comunicaciones y transportes",
        16: "Sector externo",
        17: "Finanzas públicas",
        18: "Series que ya no se actualizan"
    }

    # Si el sector no existe
    sector_nombre = sectores.get(sector, "Sector no disponible")

    # Los sectores posibles según la numeración
    banco = 'BISE'
    if sector > 4:
        banco = 'BIE'
        sector-=4

    with sync_playwright() as p:
        # Lanzamos el navegador
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.inegi.org.mx/servicios/api_indicadores.html#profile")
        page.wait_for_timeout(3500)

        # Esperamos al constructor de consultas
        page.wait_for_selector("a[aria-controls='messages']")
        page.wait_for_timeout(3500)

        # Hacemos clic en constructor
        page.click("a[aria-controls='messages']")
        page.wait_for_timeout(3500)

        # Esperamos a que el iframe esté disponible
        page.wait_for_selector("iframe#qbIndicadores")

        # Inyectamos
        page.evaluate("""
            (args) => {
                const { banco, sector } = args;
                const iframe = document.querySelector("iframe#qbIndicadores");
                if (iframe) {
                    const innerDoc = iframe.contentDocument || iframe.contentWindow.document;
                    if (innerDoc) {
                        // Seleccionamos el banco según el parámetro
                        const selectConsultaTree = innerDoc.querySelector('select#consultaTree');
                        if (selectConsultaTree) {
                            selectConsultaTree.value = banco;
                            selectConsultaTree.dispatchEvent(new Event('change', { bubbles: true }));
                        }
                        
                        // Espera de 15 segundos (15000 ms)
                        return new Promise(resolve => {
                            setTimeout(() => {
                                // Seleccionamos el sector según el número proporcionado
                                const selectTemasComponente = innerDoc.querySelector('select#temas_componente');
                                if (selectTemasComponente) {
                                    const opciones = selectTemasComponente.querySelectorAll('option');
                                    const index = sector - 1;  // Los índices empiezan en 0, pero el parámetro usa un 1-indexed
                                    if (opciones[index]) {
                                        selectTemasComponente.value = opciones[index].value;
                                        selectTemasComponente.dispatchEvent(new Event('change', { bubbles: true }));
                                    } else {
                                        console.log('El sector seleccionado no existe.');
                                    }
                                }
                                resolve();
                            }, 15000); // 15 segundos
                        });
                    }
                }
            }
        """, {"banco": banco, "sector": sector})

        page.wait_for_timeout(3500)

        # Verificamos que la opción fue seleccionada
        selected_value = page.evaluate("""
            () => {
                const iframe = document.querySelector("iframe#qbIndicadores");
                if (iframe) {
                    const innerDoc = iframe.contentDocument || iframe.contentWindow.document;
                    const selectTemasComponente = innerDoc.querySelector('select#temas_componente');
                    if (selectTemasComponente) {
                        return selectTemasComponente.value;
                    }
                }
                return null;
            }
        """)

        print(f"Opción seleccionada: {selected_value}")

        # Expansión del árbol
        page.evaluate("""
            () => {
                const iframe = document.querySelector("iframe#qbIndicadores");
                if (iframe) {
                    const innerDoc = iframe.contentDocument || iframe.contentWindow.document;
                    if (innerDoc) {
                        const expandAll = () => {
                            // Buscar todos los elementos <span> dentro del árbol que tienen la clase 'glyphicon-plus' (expandir)
                            const expanders = innerDoc.querySelectorAll("span.glyphicon-plus");
                            
                            // Si hay elementos para expandir, hacer clic en ellos
                            if (expanders.length > 0) {
                                expanders.forEach(expander => {
                                    expander.click();  // Hacer clic para expandir
                                });
                                setTimeout(expandAll, 15000);  // Llamar a la función recursivamente para continuar con los nuevos elementos expandidos
                            }
                        };
                        expandAll();  // Iniciar la expansión recursiva
                    }
                }
            }
        """)

        # Es lentísimo así que más vale esperar a que se expanda todo
        page.wait_for_timeout(60000)

        # Ahora extraemos los datos y los escribimos en un archivo CSV
        data = page.evaluate("""
            (args) => {
                const { banco, sector_nombre } = args;
                const iframe = document.querySelector("iframe#qbIndicadores");
                let result = [];
                if (iframe) {
                    const innerDoc = iframe.contentDocument || iframe.contentWindow.document;
                    if (innerDoc) {
                        const root = innerDoc.querySelector("#body_componente");  // Seleccionamos el div del que hablamos
                        if (root) {
                            const categories = root.querySelectorAll('tr');  // Buscar todos los tr dentro de la tabla
                            categories.forEach(category => {
                                const tds = category.querySelectorAll('td');
                                if (tds.length >= 2) {
                                    const category_td = tds[1];  // El segundo td es el que contiene la categoría
                                    const category_a = category_td.querySelector('a');  // Buscamos el <a> dentro de este td
                                    if (category_a) {
                                        const category_name = category_a.nextSibling.nodeValue.trim();  // Extraemos el texto de categoría entre <a> y <ul>
                                        
                                        // Expande el árbol de subcategorías
                                        const subcategories = category.querySelectorAll('ul li');
                                        subcategories.forEach(subcategory => {
                                            const subLabel = subcategory.querySelector('label');
                                            if (subLabel) {
                                                const subcategory_name = subLabel.textContent.trim();

                                                // Si tiene un checkbox, es un indicador
                                                const checkbox = subcategory.querySelector('input[type="checkbox"]');
                                                if (checkbox) {
                                                    const indicator_name = subLabel.textContent.trim();
                                                    const id = checkbox.id.split('_')[2];  // Extraemos el ID
                                                    
                                                    // Asignamos los valores en el orden correcto con subcategorías vacías
                                                    result.push([indicator_name, id, banco, sector_nombre, category_name, subcategory_name, '', '', '', '']);  // Añadimos subclase3, subclase4 y subclase5 vacíos
                                                }
                                            }
                                        });
                                    }
                                }
                            });
                        }
                    }
                }
                return result.filter(row => row[0] !== "");  // Filtrar filas donde el nombre del indicador está vacío
            }
        """, {"banco": banco, "sector_nombre": sector_nombre})

        # Comprobamos si el archivo ya existe
        file_exists = os.path.isfile(file_name)
        
        # Evitamos duplicados
        existing_data = set()
        if file_exists:
            with open(file_name, "r", encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Saltar encabezado
                existing_data = {tuple(row) for row in reader}

        # Solo agregamos las nuevas filas
        new_data = [row for row in data if tuple(row) not in existing_data]

        # Escribimos los datos en el archivo CSV
        with open(file_name, "a", newline="", encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Nombre", "ID", "BDI", "Sector", "Clase", "Subclase", "Subclase2", "Subclase3", "Subclase4", "Subclase5"])  # Orden de las columnas
            writer.writerows(new_data)

        # Y conejo
        browser.close()

# Cargamos el CSV
def load_data(filename=file_name):
    data = []
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            data.append(row)
    return headers, data

# Limpiamos la basura creada (si se creó algo) en las columnas de subcategorías
def clear_subcategories(data):
    for row in data:
        row[5] = ""  
        row[6] = ""  
        row[7] = ""  
        row[8] = ""  
        row[9] = ""  
    return data

# Asignamos subclases una después de otra
def assign_subcategories(data):
    id_map = {}  # Diccionario para guardar el ID y las filas relacionadas
    for row in data:
        indicator_id = row[1]
        
        # Si el ID ya ha sido encontrado, asignamos la clase
        if indicator_id in id_map:
            original_row = id_map[indicator_id]
            
            # Asignamos la clase del indicador duplicado a la primera subcategoría libre
            if original_row[5] == "":
                original_row[5] = row[4]  
            elif original_row[6] == "":
                original_row[6] = row[4]  
            elif original_row[7] == "":
                original_row[7] = row[4]  
            elif original_row[8] == "":
                original_row[8] = row[4]  
            elif original_row[9] == "":
                original_row[9] = row[4]  
            
            # Ahora eliminamos el duplicado (segundo indicador)
            data.remove(row)  # Borramos la fila duplicada
        else:
            # Si el ID no está en el diccionario, lo agregamos
            id_map[indicator_id] = row
    return data # se están solapando algunas clases y poniendo en desorden pero lo arreglaré con un comparador en otra función, esta ya es muy problemática

# Filtrar los datos de acuerdo al banco (BIE o BISE)
def filter_by_banco(data, banco):
    return [row for row in data if row[2] == banco]

# Contar los IDs únicos para cada banco por separado
def count_unique_ids_by_banco(data):
    # Filtrar datos para BIE
    bie_data = filter_by_banco(data, 'BIE')
    bie_ids = [row[1] for row in bie_data]
    bie_unique_ids = set(bie_ids)  # IDs únicos para BIE
    
    # Filtrar datos para BISE
    bise_data = filter_by_banco(data, 'BISE')
    bise_ids = [row[1] for row in bise_data]
    bise_unique_ids = set(bise_ids)  # IDs únicos para BISE

    # Contar IDs totales y únicos por banco
    total_bie_ids = len(bie_ids)
    total_bise_ids = len(bise_ids)
    total_unique_bie_ids = len(bie_unique_ids)
    total_unique_bise_ids = len(bise_unique_ids)

    return total_bie_ids, total_bise_ids, total_unique_bie_ids, total_unique_bise_ids

# Contar los IDs únicos
def count_unique_ids(data):
    total_bie_ids, total_bise_ids, total_unique_bie_ids, total_unique_bise_ids = count_unique_ids_by_banco(data)
    
    # Imprimir los resultados para cada banco
    print(f"BIE - IDs totales: {total_bie_ids}, IDs únicos: {total_unique_bie_ids}")
    print(f"BISE - IDs totales: {total_bise_ids}, IDs únicos: {total_unique_bise_ids}")
    
    return total_bie_ids, total_bise_ids, total_unique_bie_ids, total_unique_bise_ids

# Guardar los datos procesados en un nuevo archivo CSV
def save_data(headers, data, filename=proc_file):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

# Main para procesar el CSV
def process_csv():
    # Cargar el archivo generado
    headers, data = load_data(file_name)
    
    # Limpiar las columnas de subcategorías
    data = clear_subcategories(data)
    
    # Repetir el proceso
    total_bie_ids, total_bise_ids, total_unique_bie_ids, total_unique_bise_ids = count_unique_ids(data)
    while total_bie_ids != total_unique_bie_ids or total_bise_ids != total_unique_bise_ids:
        # Llamamos a la función de asignación de subcategorías
        data = assign_subcategories(data)
        
        # Recontamos los IDs únicos
        total_bie_ids, total_bise_ids, total_unique_bie_ids, total_unique_bise_ids = count_unique_ids(data)
        print(f"BIE - IDs totales: {total_bie_ids}, IDs únicos: {total_unique_bie_ids}")
        print(f"BISE - IDs totales: {total_bise_ids}, IDs únicos: {total_unique_bise_ids}")
        time.sleep(.25)
    
    # Guardar el archivo con los datos procesados
    save_data(headers, data, proc_file)


for i in range(1,19):
    main(i)

process_csv()

# No pensé que esto se fuera a complicar tanto para tener que usar pandas
df = pd.read_csv(proc_file)

pares_columnas = [
    (8, 9), (7, 9), (7, 8),
    (6, 9), (6, 8), (6, 7),
    (5, 9), (5, 8), (5, 7), (5, 6)
]

pares_upside_down = [
    (9, 8), (9, 7), (8, 7),
    (9, 6), (8, 6), (7, 6),
    (9, 5), (8, 5), (7, 5), (6, 5),
]

# Iteramos por cada par de filas
for i in range(len(df) - 1):  
    for col_actual, col_siguiente in pares_columnas:
        actual = df.iloc[i, col_actual]
        siguiente = df.iloc[i + 1, col_siguiente]

        if pd.notna(actual) and str(actual).strip() != "" and \
           pd.notna(siguiente) and str(siguiente).strip() != "":
            if str(actual) == str(siguiente): 
                temp = df.iloc[i + 1, col_actual]
                df.iloc[i + 1, col_actual] = df.iloc[i + 1, col_siguiente]
                df.iloc[i + 1, col_siguiente] = temp

# n vs n-1
for i in range(1, len(df)):  
    for col_actual, col_siguiente in pares_columnas:
        actual = df.iloc[i, col_actual]
        anterior = df.iloc[i - 1, col_siguiente]

        if pd.notna(actual) and str(actual).strip() != "" and \
           pd.notna(anterior) and str(anterior).strip() != "":
            if str(actual) == str(anterior): 
                temp = df.iloc[i, col_actual]
                df.iloc[i, col_actual] = df.iloc[i, col_siguiente]
                df.iloc[i, col_siguiente] = temp

# FINAL FILE
df.to_csv(final_file, index=False)
