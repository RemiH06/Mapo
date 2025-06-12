from playwright.sync_api import sync_playwright

def main():
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
            () => {
                const iframe = document.querySelector("iframe#qbIndicadores");
                if (iframe) {
                    const innerDoc = iframe.contentDocument || iframe.contentWindow.document;
                    if (innerDoc) {
                        // Esperamos a que el select "consultaTree" esté disponible
                        const selectConsultaTree = innerDoc.querySelector('select#consultaTree');
                        if (selectConsultaTree) {
                            selectConsultaTree.value = 'BISE';
                            selectConsultaTree.dispatchEvent(new Event('change', { bubbles: true }));
                        }
                        
                        // Esperamos a que el select "temas_componente" esté disponible
                        const selectTemasComponente = innerDoc.querySelector('select#temas_componente');
                        if (selectTemasComponente) {
                            // Seleccionamos el valor de "Demografía y Sociedad"
                            selectTemasComponente.value = '379_Demografía y Sociedad_6';
                            selectTemasComponente.dispatchEvent(new Event('change', { bubbles: true }));
                        }
                    }
                }
            }
        """)

        # Esperamos 3.5 segundos para asegurar que se haya ejecutado la acción
        page.wait_for_timeout(3500)

        # Verificamos que la opción "Demografía y Sociedad" fue seleccionada
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
        
        print(f"Opción seleccionada: {selected_value}")  # Esto debe imprimir "379_Demografía y Sociedad_6"

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

        # Cerramos el navegador
        browser.close()

# Ejecutamos el script
main()
