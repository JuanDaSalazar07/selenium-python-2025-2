from behave import given, when, then
from selenium import webdriver
from pages.imdb_home_page import ImdbHomePage
from pages.imdb_movie_page import ImdbMoviePage

@given('el usuario está en la página de inicio de IMDb')
def step_given_imdb_home_page(context):
    context.driver = webdriver.Chrome()  
    context.driver.get("https://www.imdb.com/")
    context.imdb_home = ImdbHomePage(context.driver)

@when('busca la película "{movie_name}" en IMDb')
def step_when_search_movie_imdb(context, movie_name):
    context.imdb_home.search_movie(movie_name)
    context.imdb_results = ImdbHomePage(context.driver)

@when('selecciona el primer resultado de IMDb')
def step_when_select_first_result_imdb(context):
    context.imdb_results.click_first_result()
    context.imdb_movie = ImdbMoviePage(context.driver)

@then('el título de la película debe ser "{expected_title}" en IMDb')
def step_then_verify_title_imdb(context, expected_title):
    actual_title = context.imdb_movie.get_movie_title()
    assert actual_title == expected_title, f"Se esperaba '{expected_title}', pero se obtuvo '{actual_title}'"

@then('la calificación debe ser "{expected_rating}" en IMDb')
def step_then_verify_rating_imdb(context, expected_rating):
    actual_rating = context.imdb_movie.get_movie_rating()
    assert actual_rating == expected_rating, f"Se esperaba '{expected_rating}', pero se obtuvo '{actual_rating}'"