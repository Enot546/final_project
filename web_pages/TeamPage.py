import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configuration.ConfigProvider import ConfigProvider


class TeamPage:
    """Класс предоставляет методы для выполнения UI-тестов на странице компании"""

    __driver: WebDriver
    __url: str
    __timeout: int

    def __init__(self, driver: WebDriver) -> None:
        """
            Создание экземпляра класса TeamPage

            :param driver: WebDriver: веб-драйвер браузера

            :return: None
        """

        self.__driver = driver
        config = ConfigProvider()
        url = config.get_ui_url()
        self.__url = url + '/team'
        self.__timeout = config.get_int('ui', 'timeout')

    @allure.step('[UI]. Перейти на страницу компании')
    def open(self) -> None:
        """
            Открытие страницы компании

            :return: None
        """

        self.__driver.get(self.__url)

    @allure.step('[UI]. Нажатие кнопки Войти')
    def login(self) -> None:
        """
            Нажать кнопку Войти

            :return: None
        """
        page_locator = 'div[class="loggedin-below loggedin-page--projects appear"]'
        btn_locator = 'form.login-form div[role="button"]'
        self.__driver.find_element(By.CSS_SELECTOR, btn_locator).click()
        WebDriverWait(self.__driver, self.__timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, page_locator)))

    @allure.step('[UI]. Получение email сотрудника')
    def get_user_email(self) -> str:
        """
            Получить email сотрудника

            :return: str: email сотрудника
        """
        WebDriverWait(self.__driver, self.__timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.cnt-main')))
        email_element = WebDriverWait(self.__driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "@")]')))
        self.__driver.execute_script("arguments[0].scrollIntoView(true);", email_element)
        return email_element.text

    @allure.step('[UI]. Получение имени сотрудника')
    def get_user_name(self) -> str:
        """
            Получить имя сотрудника

            :return: str: имя сотрудника
        """

        WebDriverWait(self.__driver, self.__timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.cnt-main')))
        return self.__driver.find_element(By.CSS_SELECTOR, 'span.truncate.user-name').text

    @allure.step('[UI]. Получение цвета кнопки Создать проект')
    def get_bg_action_color(self) -> str:
        """
            Получить CSS-атрибут цвета кнопки Создать проект

            :return: str: CSS-атрибут цвета кнопки Создать проект
        """
        btn_locator = 'div.relative div[role="button"].bg-action-default'
        return self.__driver.find_element(By.CSS_SELECTOR, btn_locator).value_of_css_property('background-color')

    @allure.step('[UI]. Получение названия проекта')
    def get_project_title(self) -> str:
        """
            Получить название первого проекта в секции Проекты компании

            :return: str: название первого проекта
        """
        card_locator = 'div[data-testid="project-card"]'
        WebDriverWait(self.__driver, self.__timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, card_locator)))
        return self.__driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="project-title"]')[0].text

    @allure.step('[UI]. Получение префикса id задач у проекта')
    def get_prefix_id_task(self) -> str:
        """
            Получить префикса id задач у первого проекта в секции Проекты компании

            :return: str: префикса id задач первого проекта
        """
        card_locator = 'div[data-testid="project-card"]'
        WebDriverWait(self.__driver, self.__timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, card_locator)))
        return self.__driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="project-card"].text-primary')[0].text

    @allure.step('[UI]. Получение текст в секции проектов')
    def get_project_section_text(self) -> str:
        """
            Получить текст в секции проектов

            :return: str: текст в секции проектов
        """
        locator = 'div.flex.flex-row.flex-wrap.gap-16'
        WebDriverWait(self.__driver, self.__timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, locator)))
        return self.__driver.find_element(By.CSS_SELECTOR, locator).text

    @allure.step('[UI]. Ввести в поле email - {email}')
    def set_email(self, email: str) -> None:
        """
            Заполнить поле email

            :param email: str: email пользователя

            :return: None
        """

        WebDriverWait(self.__driver, self.__timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.login-wnd')))
        self.__driver.find_element(By.CSS_SELECTOR, 'input[type="email"]').send_keys(email)

    @allure.step('[UI]. Ввести в поле пароль - {password}')
    def set_password(self, password: str) -> None:
        """
            Заполнить поле пароль

            :param password: str: пароль пользователя

            :return: None
        """

        WebDriverWait(self.__driver, self.__timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.login-wnd')))
        self.__driver.find_element(By.CSS_SELECTOR, 'input[type="password"]').send_keys(password)

    @allure.step('[UI]. Ввести в поле Название проекта - {project_title}')
    def set_project_title(self, project_title: str) -> None:
        """
            Заполнить поле Название проекта

            :param project_title: str: название проекта

            :return: None
        """
        input_locator = '//input[@placeholder="Введите название проекта…"]'
        WebDriverWait(self.__driver, self.__timeout).until(EC.presence_of_element_located((By.XPATH, input_locator)))
        self.__driver.find_element(By.XPATH, input_locator).send_keys(project_title)

    @allure.step('[UI]. Ввести в поле Префикс id задач - {prefix_id_task}')
    def set_prefix_id_task(self, prefix_id_task: str) -> None:
        """
            Заполнить поле Префикс id задач

            :param prefix_id_task: str: префикс id задач

            :return: None
        """
        input_locator = 'div.relative div.relative input.all-unset'
        WebDriverWait(self.__driver, self.__timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, input_locator)))
        self.__driver.find_elements(By.CSS_SELECTOR, input_locator)[1].clear()
        self.__driver.find_elements(By.CSS_SELECTOR, input_locator)[1].send_keys(prefix_id_task)

    @allure.step('[UI]. Нажатие на кнопку Добавить проект')
    def click_add_project(self) -> None:
        """
            Нажать на кнопку Добавить проект

            :return: None
        """
        locator = 'div[class="flex flex-col h-full w-fit"]'
        WebDriverWait(self.__driver, self.__timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, locator)))
        self.__driver.find_element(By.XPATH, '//span[contains(@class, "truncate") and text() = "Добавить проект с задачами"]').click()

    @allure.step('[UI]. Нажатие на кнопку Создать проект')
    def click_create_project(self, project_title: str) -> None:
        """
            Нажать на кнопку Создать проект

            :param project_title: str: название проекта

            :return: None
        """
        default_btn_locator = 'div.relative div[role="button"].bg-action-default'
        active_btn_locator = 'div.bg-action-default.rounded-8'
        new_card_locator = f'//div[contains(text(),"{project_title}")]'
        WebDriverWait(self.__driver, self.__timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, default_btn_locator)))
        self.__driver.find_elements(By.CSS_SELECTOR, active_btn_locator)[1].click()
        WebDriverWait(self.__driver, self.__timeout).until(EC.presence_of_element_located((By.XPATH, new_card_locator)))

    @allure.step('[UI]. Нажатие на иконку Три точки у проекта "{project_title}"')
    def click_three_dot(self, project_title: str) -> None:
        """
            Нажать на иконку Три точки

            :param project_title: str: название проекта

            :return: None
        """
        card = WebDriverWait(self.__driver, self.__timeout).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//div[@data-testid='project-card' and .//div[@data-testid='project-title' and contains(., '{project_title}')]]")))
        # Внутри карточки ищем кнопку меню
        menu_button = card.find_element(By.XPATH, ".//div[@data-testid='project-card-menu-button']")
        menu_button.click()

    @allure.step('[UI]. Нажатие на кнопку Удалить')
    def click_trash(self) -> None:
        """
            Нажать на кнопку Удалить

            :return: None
        """

        WebDriverWait(self.__driver, self.__timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="tooltip"]')))
        self.__driver.find_elements(By.CSS_SELECTOR, 'div[role="tooltip"] .cursor-pointer')[5].click()

    @allure.step('[UI]. Нажатие на кнопку Удалить в контекстном меню')
    def click_delete(self, project_title: str) -> None:
        """
            Нажать на кнопку Удалить в контекстном меню

            :param project_title: str: название проекта

            :return: None
        """

        locator = '//div[@class="text-left flex items-center justify-center w-full"][contains(text(),"Удалить")]'
        card_locator = f'//div[contains(text(),"{project_title}")]'
        WebDriverWait(self.__driver, self.__timeout).until(EC.presence_of_element_located((By.XPATH, locator)))
        self.__driver.find_element(By.XPATH, locator).click()
        WebDriverWait(self.__driver, self.__timeout).until(EC.invisibility_of_element_located((By.XPATH, card_locator)))

    @allure.step('[UI]. Нажатие на карточку проекта "{project_title}"')
    def click_project_card(self, project_title: str) -> None:
        """
            Нажать на Карточку проекта

            :param project_title: str: название проекта

            :return: None
        """
        card_locator = f'//div[@data-testid="project-title" and .="{project_title}"]'
        WebDriverWait(self.__driver, self.__timeout).until(EC.presence_of_element_located((By.XPATH, card_locator)))
        self.__driver.find_element(By.XPATH, card_locator).click()
