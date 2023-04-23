"""
UI test for testqastudio.me
"""
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helper.common import CommonHelper
from pom.catalog import Catalog

URL = 'https://testqastudio.me'


def test_top_menu(browser):
    """
    Test case TC-2
    """
    expected_menu = ['Каталог',  'Блог', 'О компании', 'Контакты'] #'Часто задавамые вопросы',

    main_page = Catalog(browser)
    main_page.go_to_site()
    items = main_page.get_top_menu()

    assert items == expected_menu, 'Unexpected menu list'


@pytest.mark.xfail(reason="Wait for fix bug")
def test_products_group(browser):
    """
    Test case TC-2
    """
    expected_menu = ['Все',  'Бестселлеры', 'Новые товары', 'Распродажа товаров']

    main_page = Catalog(browser)
    main_page.go_to_site()
    items = main_page.get_toolbar_menu()
    assert len(items) == len(expected_menu), "Unexpected number of products group"
    assert items == expected_menu, 'Toolbar menu does not matching to expected'

def test_count_of_all_products(browser):
    """
    Test case TC-3
    """
    expected_count = 16

    main_page = Catalog(browser)
    main_page.go_to_site()
    main_page.scroll_down()
    count_all_products = main_page.find_element((By.CSS_SELECTOR, '.found-post')).text
    main_page.find_element((By.CSS_SELECTOR, '.nav-previous-ajax')).click()
    # настройка ожидания- пока текущее количество не станет рано количеству всего
    WebDriverWait(main_page, timeout=10, poll_frequency=2).until(EC.text_to_be_present_in_element(
        ([(By.CSS_SELECTOR, ".current-post")]), count_all_products))

    elements = main_page.find_elements((By.CSS_SELECTOR, "[id='rz-shop-content'] ul li"))
    assert len(elements) == expected_count, "Unexpected count of products"

def test_right_way(browser):
    """
    Test case TC-4
    """
    main_page = Catalog(browser)
    main_page.go_to_site()
    main_page.scroll_down()
    main_page.find_element((By.CSS_SELECTOR, '.nav-previous-ajax')).click()
    WebDriverWait(main_page, timeout=10, poll_frequency=2).until(EC.text_to_be_present_in_element(([(By.CSS_SELECTOR, ".current-post")]), "16"))

    product = main_page.find_element((By.CSS_SELECTOR, "[data-product_sku='4XAVRC352']"))
    product.click()

    WebDriverWait(main_page, timeout=10, poll_frequency=2).until(EC.            visibility_of_element_located(([(By.CSS_SELECTOR, "#cart-modal")])))

    cart_is_visible = main_page.find_element((By.XPATH, "//div[@id='cart-modal']")).value_of_css_property("display")
    assert cart_is_visible == "block", "Unexpected state of cart"
    
    main_page.find_element((By.CSS_SELECTOR, "a.button.checkout")).click()
    WebDriverWait(main_page, timeout=10, poll_frequency=2).until(EC.text_to_be_present_in_element(([(By.CSS_SELECTOR, "h1.page-header__title ")]), "Оформение заказа"))
    
    #WebDriverWait(main_page, timeout=10, poll_frequency=1).until(EC.url_to_be("https://testqastudio.me/checkout/"))

    # main_page.find_element((By.CSS_SELECTOR, "a.button.checkout")).click()
    # WebDriverWait(main_page, timeout=10, poll_frequency=1).until(
    #     EC.url_to_be(URL+"/?page_id=10"))

    buyer_data_dict = {
        "billing_first_name":"Andrey",
        "billing_last_name": "Ivanov",
        "billing_address_1":"2-26, Sadovaya street",
        "billing_city": "Moscow",
        "billing_state": "Moscow",
        "billing_postcode": "122457",
        "billing_phone": "+79995784256",
        "billing_email":"andrey.i@mail.ru"   
    }
    #common_helper = CommonHelper(main_page)

    for key, value in buyer_data_dict.items(): 
        main_page.enter_input(input_id= key, data=value)
        time.sleep(1)

    # payments_el = '//*[@id="payment"] [contains(@style, "position: static; zoom: 1;")]'
    # main_page.find_element((By.XPATH, payments_el))

    # WebDriverWait(main_page, timeout=10, poll_frequency=1).until(
    #     EC.presence_of_element_located((By.XPATH, payments_el)))
    
    main_page.find_element((By.ID, "place_order")).click()
    main_page.changed_url("https://testqastudio.me/checkout/")
    # WebDriverWait(main_page, timeout=5, poll_frequency=1).until((EC.url_changes(("https://testqastudio.me/checkout/"), 'tyty')))

    result = WebDriverWait(main_page, timeout=10, poll_frequency=2).until(EC.text_to_be_present_in_element(([(By.CSS_SELECTOR, "p.woocommerce-thankyou-order-received")]), "Ваш заказ принят. Благодарим вас."))

    assert result, 'Unexpected notificztion text'