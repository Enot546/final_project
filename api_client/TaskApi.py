import allure
import requests
from requests import Response


class TaskApi:
    """Класс предоставляет методы для выполнения действий с задачами через API-запросы"""

    __url: str
    __headers: dict

    def __init__(self, base_url: str, api_key: str) -> None:
        """
            Создание экземпляра класса TaskApi
            :param base_url: str: базовый url-адрес
            :param api_key: str: ключ api
            :return: None
        """

        self.__url = base_url + '/tasks'
        self.__headers = {'Authorization': 'Bearer {api_key}'.format(api_key=api_key)}

    @allure.step('[API]. Получение задач для колонки с id {column_id}')
    def get_tasks_by_column(self, column_id: str) -> Response:
        """
            Отправляется GET-запрос для получения задач по заданной колонке
            :param column_id: str: id колонки
            :return: Response: ответ http-запроса
        """
        return requests.get(self.__url, headers=self.__headers, params={'columnId': column_id})

    @allure.step('[API]. Получение информации по задаче с id {task_id}')
    def get_task_by_id(self, task_id: str) -> Response:
        """
            Отправляется GET-запрос для получения информации по задаче
            :param task_id: str: id задачи
            :return: Response: ответ http-запроса
        """

        return requests.get(f'{self.__url}/{task_id}', headers=self.__headers)

    @allure.step('[API]. Создание задачи "{title}" в колонке с id {column_id}')
    def create_task(self, title: str, column_id: str) -> Response:
        """
            Отправляется POST-запрос для создания задачи
            :param title: str: название задачи
            :param column_id: str: id колонки
            :return: Response: ответ http-запроса
        """

        return requests.post(self.__url, headers=self.__headers, json={'title': title, 'columnId': column_id})

    @allure.step('[API]. Удаление задачи с id {id}')
    def delete_task(self, id: str) -> None:
        """
            Отправляется PUT-запрос для удаления задачи
            :param id: str: id задачи
            :return: None
        """

        requests.put('{url}/{id}'.format(url=self.__url, id=id), headers=self.__headers, json={"deleted": True})
