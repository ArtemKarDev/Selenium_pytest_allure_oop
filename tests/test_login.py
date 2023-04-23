"""
Example Selenium and pytest
"""

import pytest
#import selenium


from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://pokemonbattle.me/"

LOGINS = [
    (1,"amk86@gmail.ru","123456Po"),
    (2,"amk86@gmail.ru","123456Po"),
    (3,"amk86@mail.ru","223456Po")
]

@pytest.mark.xfail(reason="Wait for FIX bug #1")
@pytest.mark.parametrize('login', LOGINS)
def test_login_email(browser, login):
    """
    ТРК-1. Login by email
    """

    browser.get(url=URL)

    # настройка ожидания - подождать 5 сек и проверять через каждую 1 секунду пока кнопка не станет кликабельной
    WebDriverWait(browser, timeout=10, poll_frequency=1).until(EC.element_to_be_clickable((By.CLASS_NAME, "k_form_f_email")))

    email = browser.find_element(by=By.CLASS_NAME, value='k_form_f_email')
    email.click()
    email.send_keys(login[1])

    password = browser.find_element(by=By.CLASS_NAME, value='k_form_f_pass')
    password.click()
    password.send_keys(login[2])

    button = browser.find_element(by=By.CSS_SELECTOR, value='[class="k_form_button k_form_send_auth"]')
    button.click()

    if login[0] in [2,3]:
        main_error = browser.find_element(By.CSS_SELECTOR, value="[class='k_f_error_text k_main_error_text']")
        # настройка ожидания - когда искомы элемент будет с определенным текстом
        WebDriverWait(browser, timeout=5, poll_frequency=1).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[class='k_f_error_text k_main_error_text']"),
                                            'Неверные логин или пароль'))
        assert main_error.text == 'Неверные логин или пароль', 'Unexpected error text'
    else:
        trainer = browser.find_element(by=By.CSS_SELECTOR, value='[class="id_number k_trainer_id"]')

        # настройка ожидания - подождать 5 сек и проверять через каждую 1 секунду пока кнопка не станет кликабельной
        WebDriverWait(browser, timeout=5, poll_frequency=1).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '[class="id_number k_trainer_id"]'), "3386"))
        trainer = browser.find_element(by=By.CSS_SELECTOR, value='[class="id_number k_trainer_id"]')

        assert trainer.text == "3386", "Unexpected trainer ID"
        exit = browser.find_element(By.CSS_SELECTOR, value='[class="top_menu_exit"] a')
        exit.click()

