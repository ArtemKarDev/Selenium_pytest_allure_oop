"""
Test first
"""

import pytest

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pom.catalog import Catalog


URL = 'https://testqastudio.me/'

vendor_code = "C0MSSDSUM7" # C0MSSDSUMK 


def test_product_view_sku(browser):
    """
    Test case WERT-1: 
    Открытие деталей товара. Проверка артикула    
    """
    main_page = Catalog(browser)
    main_page.go_to_site()
    main_page.find_element((By.CSS_SELECTOR, '.tab-best_sellers')).click()
    main_page.find_element((By.CSS_SELECTOR, '.post-11094')).click()
    sku = main_page.find_element((By.CSS_SELECTOR,".sku"))
    assert sku.text == 'C0MSSDSUMK', "Unexpected sku"
    

