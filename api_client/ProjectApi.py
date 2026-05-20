import allure
import requests
from requests import Response


class ProjectApi:
    """Класс предоставляет методы для выполнения действий с проектами через API-запросы"""

    __url: str
    __headers: dict

    def __init__(self, base_url: str, api_key: str) -> None:
        """
            Создание экземпляра класса ProjectApi
            :param base_url: str: базовый url-адрес
            :param api_key: str: ключ api
            :return: None
        """
        self.__url = base_url + '/projects'
        self.__headers = {'Authorization': 'Bearer {api_key}'.format(api_key=api_key)}

    @allure.step('[API]. Получение проектов компании')
    def get_projects(self) -> Response:
        """
            Отправляется GET-запрос для получения проектов
            :return: Response: ответ http-запроса
        """
        return requests.get(self.__url, headers=self.__headers)

    @allure.step('[API]. Получение информации по проекту с id {id}')
    def get_project_by_id(self, id: str) -> Response:
        """
            Отправляется GET-запрос для получения информации по проекту
            :param id: str: id проекта
            :return: Response: ответ http-запроса
        """

        return requests.get('{url}/{id}'.format(url=self.__url, id=id), headers=self.__headers)

    @allure.step('[API]. Создание проекта с названием "{title}"')
    def create_project(self, title: str, api_key: str | None = None, users_dict: dict | None = None) -> Response:
        """
            Отправляется POST-запрос для создания проекта
            :param title: str: название проекта
            :param api_key: str | None: (optional) ключ api
            :param users_dict: dict | None: (optional) роли пользователя в формате "user_id":"role"
            :return: Response: ответ http-запроса
        """

        headers = ''
        if api_key == None:
            headers = self.__headers
        else:
            headers = {'Authorization': f'Bearer {api_key}'}

        body = {
            'title': title,
            'users': users_dict
        }

        return requests.post(self.__url, headers=headers, json=body)

    @allure.step('[API]. Удаление проекта с id {id}')
    def delete_project(self, id: str) -> None:
        """
            Отправляется PUT-запрос для удаления проекта
            :param id: str: id проекта
            :return: None
        """

        requests.put('{url}/{id}'.format(url=self.__url, id=id), headers=self.__headers, json={"deleted": True})
