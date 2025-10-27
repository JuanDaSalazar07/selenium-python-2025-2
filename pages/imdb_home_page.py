from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ImdbHomePage(BasePage):
    SEARCH_INPUT = (By.ID, 'suggestion-search')
    SEARCH_BUTTON = (By.ID, 'suggestion-search-button')
    FIRST_RESULT = (By.XPATH, "//li[contains(@class, 'ipc-metadata-list-summary-item')]//a")

    def search_movie(self, movie_name):
        self.enter_text(self.SEARCH_INPUT, movie_name)
        self.click(self.SEARCH_BUTTON)

    def click_first_result(self):
        self.click(self.FIRST_RESULT)
