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

        
        search_input = None
        try:
            search_input = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input#suggestion-search, input[name='q']"))
            )
        except TimeoutException:
            
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            for inp in inputs:
                if inp.is_displayed() and inp.get_attribute("type") in (None, "text", "search"):
                    search_input = inp
                    break

        if not search_input:
            raise AssertionError("Caja de búsqueda no encontrada en la página de inicio de IMDb")

        search_input.clear()
        search_input.send_keys(movie_name)

        
        try:
            search_input.send_keys(Keys.ENTER)
        except Exception:
            try:
                search_input.submit()
            except Exception:
                pass  

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
                
                el = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, sel)))
                el.click()
                return
            except Exception as e:
                last_exception = e
                
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

        
        raise AssertionError("No se pudo clicar el primer resultado de IMDb") from last_exception
