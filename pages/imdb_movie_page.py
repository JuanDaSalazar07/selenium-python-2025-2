from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class ImdbMoviePage:
    def __init__(self, driver, timeout=12):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_title(self):
        # Espera que alguna forma del título esté visible
        selectors = [
            "h1[data-testid='hero-title-block__title']",
            "div.title_wrapper > h1",
            "h1"
        ]
        for sel in selectors:
            try:
                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, sel)))
                return
            except TimeoutException:
                continue
        raise TimeoutException("Título no visible en la página de movie")

    def get_movie_title(self):
        """
        Recupera el título de la película usando varios selectores como fallback.
        """
        selectors = [
            "h1[data-testid='hero-title-block__title']",   # diseño moderno
            "div.title_wrapper > h1",                       # diseño clásico
            "h1"                                            # fallback genérico
        ]
        for sel in selectors:
            try:
                el = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, sel)))
                text = el.text
                if text:
                    return text
            except Exception:
                continue
        raise AssertionError("No se pudo obtener el título de la película en la página de IMDb")

    def get_movie_rating(self):
        """
        Recupera la calificación (rating) de la película con varios selectores.
        Devuelve la calificación como string (por ejemplo '8.2').
        """
        selectors = [
            "div[data-testid='hero-rating-bar__aggregate-rating__score'] span",  # diseño moderno
            "span[itemprop='ratingValue']",                                      # diseño clásico
            "div.ratingValue > strong > span"                                    # otro fallback
        ]
        for sel in selectors:
            try:
                el = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, sel)))
                text = el.text
                if text:
                    # Normalizar: quitar espacios y posibles barras
                    return text.strip()
            except Exception:
                continue
        # Si no hay rating visible, devolver cadena vacía
        return ""