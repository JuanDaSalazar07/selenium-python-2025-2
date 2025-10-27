from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class ImdbHomePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def search_movie(self, movie_name):
        """
        Escribe en la caja de búsqueda y dispara la búsqueda (Enter).
        Usa selectores robustos y fallback si la estructura cambia.
        """
        from selenium.webdriver.common.keys import Keys

        # Intentar selector moderno
        search_input = None
        try:
            search_input = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input#suggestion-search, input[name='q']"))
            )
        except TimeoutException:
            # Fallback más amplio: tomar el primer input visible
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            for inp in inputs:
                if inp.is_displayed() and inp.get_attribute("type") in (None, "text", "search"):
                    search_input = inp
                    break

        if not search_input:
            raise AssertionError("Caja de búsqueda no encontrada en la página de inicio de IMDb")

        search_input.clear()
        search_input.send_keys(movie_name)

        # Intentar presionar Enter para ir a resultados
        try:
            search_input.send_keys(Keys.ENTER)
        except Exception:
            try:
                search_input.submit()
            except Exception:
                pass  # si no se puede enviar, confiar en sugerencias que se mostrarán

    def click_first_result(self):
        """
        Hace clic en el primer resultado de la búsqueda. Soporta:
        - resultados en dropdown (sugerencias)
        - página de resultados con enlaces a /title/
        Implementa múltiples selectores y fallback a elementos visibles.
        """
        selectors = [
            "div.imdb-header__search-menu a[href*='/title/']",
            ".react-autosuggest__suggestions-list a[href*='/title/']",
            "td.result_text > a",
            ".findList .result_text a",
            "div.findSection a[href*='/title/']",
            "a[href*='/title/']"
        ]

        last_exception = None
        for sel in selectors:
            try:
                # intentar esperar y clicar el primer elemento clicable del selector
                el = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, sel)))
                el.click()
                return
            except Exception as e:
                last_exception = e
                # fallback: intentar obtener todos los elementos y clicar el primero visible
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, sel)
                    for e2 in elements:
                        try:
                            if e2.is_displayed():
                                e2.click()
                                return
                        except Exception:
                            continue
                except Exception:
                    continue

        # Si llega aquí, no se pudo clicar ningún elemento útil
        raise AssertionError("No se pudo clicar el primer resultado de IMDb") from last_exception
