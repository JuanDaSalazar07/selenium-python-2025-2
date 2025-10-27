from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.imdb_home_page import ImdbHomePage
from pages.imdb_movie_page import ImdbMoviePage

@given('el usuario está en la página de inicio de IMDb')
def step_given_imdb_home_page(context):
    # Reusar driver si ya existe (útil para debugging/local runs)
    if hasattr(context, "driver") and context.driver:
        context.driver.get("https://www.imdb.com/")
    else:
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument("--headless=new")  # descomenta para headless
        context.driver = webdriver.Chrome(service=Service(), options=chrome_options)
        context.driver.implicitly_wait(2)
        context.driver.get("https://www.imdb.com/")
    context.imdb_home = ImdbHomePage(context.driver)

@when('busca la película "{movie_name}" en IMDb')
def step_when_search_movie_imdb(context, movie_name):
    # Ensured in page object: escribe y envía (Enter) con fallback
    context.imdb_home.search_movie(movie_name)

@when('selecciona el primer resultado de IMDb')
def step_when_select_first_result_imdb(context):
    # Hacer clic en el primer resultado y esperar que la página de película cargue
    context.imdb_home.click_first_result()

    # Inicializar page object de movie y esperar título visible
    context.imdb_movie = ImdbMoviePage(context.driver)
    try:
        # Esperar hasta que alguna versión del título sea visible
        context.imdb_movie.wait_for_title()
    except TimeoutException as e:
        raise AssertionError("La página de la película no cargó correctamente después de seleccionar el resultado") from e

@then('el título de la película debe ser "{expected_title}" en IMDb')
def step_then_verify_title_imdb(context, expected_title):
    actual_title = context.imdb_movie.get_movie_title().strip()
    # Normalizar espacios y año si viene en el título
    if actual_title.endswith(")"):
        # eliminar año final si aparece entre paréntesis al final
        import re
        actual_title = re.sub(r"\s*\(\d{4}\)\s*$", "", actual_title).strip()
    assert actual_title == expected_title, f"Se esperaba '{expected_title}', pero se obtuvo '{actual_title}'"

@then('la calificación debe ser "{expected_rating}" en IMDb')
def step_then_verify_rating_imdb(context, expected_rating):
    actual_rating = context.imdb_movie.get_movie_rating().strip()

    # Si la expectativa y el valor real están vacíos, pasar
    if not expected_rating.strip() and not actual_rating:
        return

    # Intentar comparar numéricamente aceptando ',' o '.' como separador decimal
    try:
        exp_f = float(expected_rating.replace(',', '.').strip())
        act_f = float(actual_rating.replace(',', '.').strip())
        # comparar con tolerancia pequeña para evitar problemas de representación
        if abs(act_f - exp_f) < 0.05:
            return
        else:
            raise AssertionError(f"Se esperaba '{expected_rating}', pero se obtuvo '{actual_rating}'")
    except ValueError:
        # Fallback: comparar cadenas normalizando separadores
        norm_expected = expected_rating.replace(',', '.').strip()
        norm_actual = actual_rating.replace(',', '.').strip()
        assert norm_actual == norm_expected, f"Se esperaba '{expected_rating}', pero se obtuvo '{actual_rating}'"