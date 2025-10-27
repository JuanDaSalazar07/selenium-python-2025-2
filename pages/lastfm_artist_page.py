from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LastFmArtistPage(BasePage):
    LATEST_RELEASE_DATE = (By.CLASS_NAME, "artist-header-featured-items-item-date")  
    
    def get_latest_release_date(self):
        
        element = self.find_element(self.LATEST_RELEASE_DATE)
        
        return element.text.strip()  