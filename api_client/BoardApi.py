import allure
import requests
from requests import Response


class BoardApi:
    """Класс предоставляет методы для выполнения действий с досками через API-запросы"""

    __url: str
    __headers: dict

    def __init__(self, base_url: str, api_key: str) -> None:
        """
            Создание экземпляра класса BoardApi
            :param base_url: str: базовый url-адрес
            :param api_key: str: ключ api
            :return: None
        """

        self.__url = base_url + '/boards'
        self.__headers = {'Authorization': 'Bearer {api_key}'.format(api_key=api_key)}

    @allure.step('[API]. Создание доски "{title}" для проекта с id {project_id}')
    def create_board(self, title: str, project_id: str) -> Response:
        """
            Отправляется POST-запрос для создания доски для заданного проекта
            :param title: str: название доски
            :param project_id: str: id проекта
            :return: Response: ответ http-запроса
        """

        return requests.post(self.__url, headers=self.__headers, json={'title': title, 'projectId': project_id})

    @allure.step('[API]. Удаление доски с id {id}')
    def delete_board(self, id: str) -> None:
        """
            Отправляется PUT-запрос для удаления доски
            :param id: str: id доски
            :return: None
        """

        requests.put('{url}/{id}'.format(url=self.__url, id=id), headers=self.__headers, json={"deleted": True})
