import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configuration.ConfigProvider import ConfigProvider


class IndexPage:
    """Класс предоставляет методы для выполнения UI-тестов на главной странице"""

    __driver: WebDriver
    __url: str
    __timeout: int

    def __init__(self, driver: WebDriver) -> None:
        """
            Создание экземпляра класса IndexPage
            :param driver: WebDriver: веб-драйвер браузера
            :return: None
        """

        self.__driver = driver
        config = ConfigProvider()
        self.__url = config.get_ui_url()
        self.__timeout = config.get_int('ui', 'timeout')

    @allure.step('[UI]. Перейти на главную страницу сайта')
    def open(self) -> None:
        """
            Открытие главной страницы
            :return: None
        """

        self.__driver.get(self.__url)
        WebDriverWait(self.__driver, self.__timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#header')))

    @allure.step('[UI]. Нажатие кнопки Войти')
    def click_sign_in(self) -> None:
        """
            Нажать кнопку Войти
            :return: None
        """

        self.__driver.find_element(By.CSS_SELECTOR, 'a.sign-in-button').click()
