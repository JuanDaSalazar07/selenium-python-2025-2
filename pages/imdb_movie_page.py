from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ImdbMoviePage(BasePage):
    
    MOVIE_TITLE = (By.CSS_SELECTOR, "h1")
    MOVIE_RATING = (By.XPATH, "//span[@itemprop='ratingValue']")

    def get_movie_title(self):
       
        return self.find_element(self.MOVIE_TITLE).text

    def get_movie_rating(self):
        
        element = self.find_element(self.MOVIE_RATING)
        return element.text.strip() 