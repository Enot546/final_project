import pytest
import allure
import random
import string
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options
from collections.abc import Generator
from api_client.AuhtApi import AuthApi
from api_client.UserApi import UserApi
from api_client.ProjectApi import ProjectApi
from api_client.BoardApi import BoardApi
from api_client.ColumnApi import ColumnApi
from api_client.TaskApi import TaskApi
from configuration.ConfigProvider import ConfigProvider
from testdata.DataProvider import DataProvider
from web_pages.TeamPage import TeamPage


@pytest.fixture()
def browser() -> Generator[WebDriver]:
    with allure.step('Открыть и настроить браузер'):
        config = ConfigProvider()
        timeout = config.get_int('ui', 'timeout')
        browser_name = config.get('ui', 'browser_name')

        if browser_name == 'chrome':
            browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        else:
            options = Options()
            options.page_load_strategy = 'normal'
            browser = webdriver.Firefox(options=options)

        browser.implicitly_wait(timeout)
        browser.maximize_window()
        yield browser

    with allure.step('Закрыть браузер'):
        browser.quit()


@pytest.fixture
def auth_browser(browser, test_data: DataProvider) -> WebDriver:
    with allure.step('Создать экземпляр веб-драйвера браузера'):
        team_page = TeamPage(browser)
        team_page.open()
        team_page.set_email(test_data.get('email'))
        team_page.set_password(test_data.get('password'))
        team_page.login()
        return browser


@pytest.fixture(scope="session")
def auth_api() -> AuthApi:
    data_provider = DataProvider()
    return AuthApi(ConfigProvider().get_api_url(), data_provider.get('email'), data_provider.get('password'))


@pytest.fixture(scope="session")
def user_api() -> UserApi:
    return UserApi(ConfigProvider().get_api_url(), DataProvider().get_api_key())


@pytest.fixture(scope="session")
def project_api() -> ProjectApi:
    return ProjectApi(ConfigProvider().get_api_url(), DataProvider().get_api_key())


@pytest.fixture(scope="session")
def board_api() -> BoardApi:
    return BoardApi(ConfigProvider().get_api_url(), DataProvider().get_api_key())


@pytest.fixture(scope="session")
def column_api() -> ColumnApi:
    return ColumnApi(ConfigProvider().get_api_url(), DataProvider().get_api_key())


@pytest.fixture(scope="session")
def task_api() -> TaskApi:
    return TaskApi(ConfigProvider().get_api_url(), DataProvider().get_api_key())


@pytest.fixture(scope="session")
def test_data() -> DataProvider:
    return DataProvider()


@pytest.fixture
def create_utility_project(
    project_api: ProjectApi,
    generate_random_str: str,
    delete_utility_project: dict
):
    with allure.step('Создать тестовые данные - добавить проект'):
        data = {
            'project_title': f'{generate_random_str} {str(random.randint(0, 99999))}',
            'project_id': ''
        }
        project_id = project_api.create_project(data['project_title']).json()['id']
        data['project_id'] = project_id
        yield data

    delete_utility_project['project_id'] = data['project_id']


@pytest.fixture
def delete_utility_project(project_api: ProjectApi):
    with allure.step('Очистить тестовые данные - удалить проект'):
        data = {'project_id': ''}
        yield data

    project_api.delete_project(data['project_id'])


@pytest.fixture
def delete_utility_board(board_api: BoardApi):
    with allure.step('Очистить тестовые данные - удалить доску'):
        data = {
            'first_board_id': '',
            'second_board_id': ''
        }
        yield data

    board_api.delete_board(data['first_board_id'])
    board_api.delete_board(data['second_board_id'])


@pytest.fixture
def delete_utility_column(column_api: ColumnApi):
    with allure.step('Очистить тестовые данные - удалить колонку'):
        data = {'column_id': ''}
        yield data

    column_api.delete_column(data['column_id'])


@pytest.fixture
def delete_utility_task(task_api: TaskApi):
    with allure.step('Очистить тестовые данные - удалить задачу'):
        data = {'task_id': ''}
        yield data

    task_api.delete_task(data['task_id'])


@pytest.fixture
def generate_random_str() -> str:
    with allure.step('Генерирование уникальной строки'):
        return ''.join(random.choices(string.ascii_lowercase, k=5))
