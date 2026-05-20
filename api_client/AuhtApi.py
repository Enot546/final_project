import allure
import requests
from requests import Response


class AuthApi:
    """Класс предоставляет методы для отправки API-запросов на авторизацию"""

    __url: str
    __login: str
    __password: str

    def __init__(self, base_url: str, login: str, password: str) -> None:
        """
            Создание экземпляра класса AuthApi
            :param base_url: str: базовый url-адрес
            :param login: str: логин пользователя
            :param password: str: (optional) пароль пользователя
            :return: None
        """

        self.__url = base_url + '/auth/keys'
        self.__login = login
        self.__password = password

    @allure.step('[API]. Получение списка ключей api для компании')
    def get_api_keys(self, company_id: str) -> list[dict]:
        """
            Отправлеяется POST-запрос для получение достпуных ключей api
            :param company_id: str: id компании
            :return: list[dict]: список объектов, содержащих информацию о ключах api
        """

        body = {
            'login': self.__login,
            'password': self.__password,
            'companyId': company_id
        }
        return requests.post(f'{self.__url}/get', json=body)

    @allure.step('[API]. Создание нового ключа api')
    def create_api_key(self, company_id: str) -> Response:
        """
            Отправлеяется POST-запрос для создания нового ключа api
            :param company_id: str: id компании
            :return: Response: ответ http-запроса
        """

        body = {
            'login': self.__login,
            'password': self.__password,
            'companyId': company_id
        }
        return requests.post(self.__url, json=body)

    @allure.step('[API]. Удаление ключа api - {api_key}')
    def delete_api_key(self, api_key: str) -> None:
        """
            Отправлеяется DELETE-запрос для удаления ключа api
            :param api_key: str: ключа api
            :return: None
        """

        requests.delete(f'{self.__url}/{api_key}')
