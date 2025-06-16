import csv
import os
from playwright.sync_api import sync_playwright

def main(sector):
    # Los sectores posibles según la numeración
    banco = 'BISE'
    if sector > 4:
        banco = 'BIE'
    
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

    # Si el sector no existe, mostramos un mensaje
    sector_nombre = sectores.get(sector, "Sector no disponible")

    with sync_playwright() as p:
        # Lanzamos el navegador
        browser = p.chromium.launch(headless=False)  # Si quieres ver la navegación, pon headless=False
        page = browser.new_page()

        # Vamos a la URL principal
        page.goto("https://www.inegi.org.mx/servicios/api_indicadores.html#profile")
        
        # Esperamos 3.5 segundos para que la página cargue
        page.wait_for_timeout(3500)

        # Esperamos a que el enlace "Constructor de Consultas" esté disponible
        page.wait_for_selector("a[aria-controls='messages']")
        
        # Esperamos 3.5 segundos más
        page.wait_for_timeout(3500)

        # Hacemos clic en el enlace "Constructor de Consultas"
        page.click("a[aria-controls='messages']")

        # Esperamos 3.5 segundos para asegurarnos de que la acción de clic haya terminado
        page.wait_for_timeout(3500)

        # Esperamos a que el iframe esté disponible
        page.wait_for_selector("iframe#qbIndicadores")

        # Ahora inyectamos el código para interactuar dentro del iframe
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
                    }
                }
            }
        """, {"banco": banco, "sector": sector})

        # Esperamos 3.5 segundos para asegurar que se haya ejecutado la acción
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

        print(f"Opción seleccionada: {selected_value}")  # Imprime la opción seleccionada

        # Expande todas las clases dentro del árbol y sus subclases recursivamente
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

        # Esperamos 15 segundos entre cada expansión y damos un tiempo total de 60 segundos antes de cerrar el navegador
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
                        const items = innerDoc.querySelectorAll('li');
                        items.forEach(item => {
                            const label = item.querySelector('label');
                            const checkbox = item.querySelector('input[type="checkbox"]');
                            if (label && checkbox) {
                                const id = checkbox.id.split('_')[2];  // Extraemos el ID
                                const name = label.textContent.trim();  // Extraemos el nombre
                                
                                // Extraemos las categorías y subcategorías
                                let category = '';
                                let subcategory = '';
                                const parentLabel = item.closest('ul').previousElementSibling;
                                if (parentLabel && parentLabel.tagName === 'LABEL') {
                                    category = parentLabel.textContent.trim();
                                }
                                
                                const grandParentLabel = item.closest('ul').parentElement.previousElementSibling;
                                if (grandParentLabel && grandParentLabel.tagName === 'LABEL') {
                                    subcategory = grandParentLabel.textContent.trim();
                                }
                                
                                result.push([name, id, banco, sector_nombre, category, subcategory]);  // Agregamos la categoría y subcategoría
                            }
                        });
                    }
                }
                return result;
            }
        """, {"banco": banco, "sector_nombre": sector_nombre})

        file_exists = os.path.isfile("test2.csv")
        
        existing_data = set()
        if file_exists:
            with open("test2.csv", "r", encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Saltar encabezado
                existing_data = {tuple(row) for row in reader}

        new_data = [row for row in data if tuple(row) not in existing_data]

        with open("test2.csv", "a", newline="", encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["nombre", "id", "bdi", "sect", "cat", "subcat"])
            writer.writerows(new_data)

        # Cerramos el navegador
        browser.close()

main(1)
#for i in range(1,19):
#    main(i)
