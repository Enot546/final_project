import allure
import requests


class UserApi:
    """Класс предоставляет методы для выполнения действий с пользователями через API-запросы"""

    __url: str
    __headers: dict

    def __init__(self, base_url: str, api_key: str) -> None:
        """
            Создание экземпляра класса UserApi
            :param base_url: str: базовый url-адрес
            :param api_key: str: ключ api
            :return: None
        """
        self.__url = base_url + '/users'
        self.__headers = {'Authorization': 'Bearer {api_key}'.format(api_key=api_key)}

    @allure.step('[API]. Получение id пользователя с email {email}')
    def get_user_id(self, email: str) -> str:
        """
            Отправляется GET-запрос для получения id пользователя
            :param email: str: email пользователя
            :return: str: id пользователя
        """

        return requests.get(self.__url, headers=self.__headers, params={'email': email}).json()['content'][0]['id']
