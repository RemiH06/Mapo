from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        # Lanzamos el navegador
        browser = p.chromium.launch(headless=False) 
        page = browser.new_page()

        # Vamos a la URL principal
        page.goto("https://www.inegi.org.mx/servicios/api_indicadores.html#profile")
        page.wait_for_timeout(3500)

        # Esperamos a que el enlace "Constructor de Consultas" esté disponible
        page.wait_for_selector("a[aria-controls='messages']")
        page.wait_for_timeout(3500)

        # Hacemos clic en el enlace "Constructor de Consultas"
        page.click("a[aria-controls='messages']")
        page.wait_for_timeout(3500)

        # Esperamos a que el iframe esté disponible
        page.wait_for_selector("iframe#qbIndicadores")

        # Y le inyectamos selección del banco de indicadores
        page.evaluate("""
            () => {
                const iframe = document.querySelector("iframe#qbIndicadores");
                if (iframe) {
                    const innerDoc = iframe.contentDocument || iframe.contentWindow.document;
                    if (innerDoc) {
                        // Esperamos a que el select esté disponible
                        const select = innerDoc.querySelector('select#consultaTree');
                        if (select) {
                            // Cambiamos el valor del select para elegir la opción "Banco de Indicadores"
                            select.value = 'BISE';
                            // Disparamos el evento change para que la acción se registre
                            const event = new Event('change', { bubbles: true });
                            select.dispatchEvent(event);
                        }
                    }
                }
            }
        """)

        page.wait_for_timeout(3500)

        # Validamos
        selected_value = page.evaluate("""
            () => {
                const iframe = document.querySelector("iframe#qbIndicadores");
                if (iframe) {
                    const innerDoc = iframe.contentDocument || iframe.contentWindow.document;
                    const select = innerDoc.querySelector('select#consultaTree');
                    if (select) {
                        return select.value;
                    }
                }
                return null;
            }
        """)
        
        print(f"Opción seleccionada: {selected_value}")
        browser.close()

main()
