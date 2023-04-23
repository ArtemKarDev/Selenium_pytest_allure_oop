
"""
POM base
"""
from loguru import logger

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = 'https://testqastudio.me/'

class TMLocators:
    """
    Class for locators
    """

    # top menu item
    TM_CATALOG = (By.CSS_SELECTOR, '#page [class*="menu-item-10076"]')
    TM_FAQ = (By.CSS_SELECTOR, '#page [class*="menu-item=11088"]')
    TM_BLOG = (By.CSS_SELECTOR, '#page [class*="menu-item-58"]')
    TM_ABOUT = (By.CSS_SELECTOR, '#page [class*="menu-item-6059"]')
    TM_CONTACTS = (By.CSS_SELECTOR, '#page [class*="menu-item-6110"]')

    # base locator for top menu
    TM = (By.CSS_SELECTOR, '[id="menu-primary-menu" ] li a')

    # base locator for toolbar menu on catalog page
    TB = (By.CSS_SELECTOR, '[class="catalog-toolbar-tabs__content"] a')

    # toolbar product group menu item
    TB_ALL = (By.CSS_SELECTOR, '[class*="tab-all active"]')
    TB_BEST = (By.CSS_SELECTOR, '[class*="tab-best_sellers "]')
    TB_NEW = (By.CSS_SELECTOR, '[class*="tab-new "]')
    TB_SALE = (By.CSS_SELECTOR, '[class*="tab-sale "]')



class BasePage:
    """
    Base page
    """
    def __init__(self, driver):
        self.driver = driver
        self.base_url = URL

    def find_element(self, locator, time=10):
        """
        Find element with waiting
        """
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator),
                                                        message=f'Can`t find element by locator {locator}')
    
    def find_elements(self, locator, time=10):
        """
        Find elements with waiting
        """
        return WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(locator),
                                                        message=f'Can`t find element by locator {locator}') 

    def scroll_down(self):
        """
        Scroll
        """        
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def go_to_site(self):
        """
        Get base URL
        """
        return self.driver.get(self.base_url)
    
    def go_to_catalog(self):
        """
        Go to catalog
        """
        self.find_element(locator=TMLocators.TM_CATALOG).click()

    def go_to_faq(self):
        """
        Go to FAQ
        """
        logger.info('Find element')
        self.find_element(locator=TMLocators.TM_FAQ).click()
        logger.info('Wait for page')
        WebDriverWait(self.driver, time=5, poll_frequency=1).until(EC.url_to_be(URL+"faq/"))

    def get_current_url(self):
        """
        Get current url from
        """
        return self.driver.current_url
    
    def changed_url(self, url, time=10):
        """
        check changed  url 
        """
        wait = WebDriverWait(self, time)
        desired_url = url
        return wait.until(lambda self: self.get_current_url() == desired_url)


        return WebDriverWait(self.driver, time, poll_frequency=1).until(EC.url_changes(url))
        
    
    def get_top_menu(self) -> list:
        """
        Get top menu item
        """
        elements = self.find_elements(locator=TMLocators.TM)

        result_list = []
        for element in elements:
            result_list.append(element.text)

        return result_list
    
    def get_toolbar_menu(self) -> list:
        """
        Get toolbar menu item
        """
        elements = self.find_elements(locator=TMLocators.TB)

        result_list = []
        for element in elements:
            result_list.append(element.text)

        return result_list

    def enter_input(self,input_id, data):
        """
        Method for input
        """
        input_field = self.find_element(locator=(By.ID,input_id))
        input_field.click()
        input_field.send_keys(data)
        return input_field
    
    

    def go_to_blog(self):
        """
        Go to BLOG
        """
        self.find_element(locator=TMLocators.TM_BLOG).click()
        WebDriverWait(self.driver, time=5, poll_frequency=1).until(EC.url_to_be(URL+"blogs/"))

    
    def go_to_about(self):
        """
        Go to ABOUT
        """
        self.find_element(locator=TMLocators.TM_ABOUT).click()
        WebDriverWait(self.driver, time=5, poll_frequency=1).until(EC.url_to_be(URL+"about-us/"))

    def go_to_contacts(self):
        """
        Go to CONTACTS
        """
        self.find_element(locator=TMLocators.TM_CONTACTS).click()
        WebDriverWait(self.driver, time=5, poll_frequency=1).until(EC.url_to_be(URL+"contact-us/"))
