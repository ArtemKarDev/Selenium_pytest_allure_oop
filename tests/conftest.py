"""
Fixture  Configuration test 
"""
import pytest

#import os
#from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session") # декаратор с помощью которого последующая функция с конфигами распространяется на сессию
def browser():
    """
    Main fixture
    """
    # Опции запуска браузера
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("start-maximized")     # открываем на полный экран
    chrome_options.add_argument("--disable-infobars")  # отключаем инфо сообщения
    chrome_options.add_argument("--disable-extensions")     # отключаем расширения
    chrome_options.add_argument("--disable-gpu")  # применять только программные средства ОС
    chrome_options.add_argument("--disable-dev-shm-usage")  #  преодолеть проблемы с ограниченными ресурсами
    # chrome_options.add_argument("--headless")     # спец режим "без браузера"

    # устанавливаем webdrive в соответсвии с версией используемого браузера
    # https://github.com/SergeyPirogov/webdriver_manager/blob/master/README.md
    service = Service(ChromeDriverManager().install())
    # запускаем браузер с указанными выше настройками
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver    # в случае падения теста принудительно закрывает окна браузера
    driver.quit()

# @pytest.fixture()
# def clear_report():
#     """
#     Clear all allure reports
#     """
#     path = f"{os.getcwd()}\allure_results\\"
#     for file_name in os.listdir(path):
#         file = path + file_name
#         if os.path.isfile(file):
#             logger.info(f'Deleting file: {file}')
#             os.remove(file)
