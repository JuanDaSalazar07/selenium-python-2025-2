from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LastFmHomePage(BasePage):
    SEARCH_ICON = (By.CLASS_NAME, 'masthead-search-toggle')
    SEARCH_INPUT = (By.ID, 'masthead-search-field')
    SEARCH_BIN = (By.CLASS_NAME, 'masthead-search-submit')

    def search_artist(self, artist_name):
        self.click(self.SEARCH_ICON) 
        self.enter_text(self.SEARCH_INPUT, artist_name)  
        self.click(self.SEARCH_BIN) 