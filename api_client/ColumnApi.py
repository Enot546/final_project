import allure
import requests
from requests import Response


class ColumnApi:
    """Класс предоставляет методы для выполнения действий с колонками через API-запросы"""

    __url: str
    __headers: dict

    def __init__(self, base_url: str, api_key: str) -> None:
        """
            Создание экземпляра класса ColumnApi
            :param base_url: str: базовый url-адрес
            :param api_key: str: ключ api
            :return: None
        """

        self.__url = base_url + '/columns'
        self.__headers = {'Authorization': 'Bearer {api_key}'.format(api_key=api_key)}

    @allure.step('[API]. Создание колонки "{title}" для доски с id {board_id}')
    def create_column(self, title: str, board_id: str) -> Response:
        """
            Отправляется POST-запрос для создания колонки для заданной доски
            :param title: str: название колонки
            :param board_id: str: id доски
            :return: Response: ответ http-запроса
        """

        return requests.post(self.__url, headers=self.__headers, json={'title': title, 'boardId': board_id})

    @allure.step('[API]. Обновление колонки с id {column_id}, обновленные данные {body}')
    def update_column(self, column_id: str, body: dict) -> Response:
        """
            Отправляется PUT-запрос для обновления колонки
            :param column_id: str: id колонки
            :param body: dict: тело запроса для обновления
            :return: Response: ответ http-запроса
        """

        return requests.put(f'{self.__url}/{column_id}', headers=self.__headers, json=body)

    @allure.step('[API]. Получение информации по колонке с id {column_id}')
    def get_column_by_id(self, column_id: str) -> Response:
        """
            Отправляется GET-запрос для получения информации по колонке
            :param column_id: str: id колонки
            :return: Response: ответ http-запроса
        """

        return requests.get(f'{self.__url}/{column_id}', headers=self.__headers)

    @allure.step('[API]. Удаление колонки с id {id}')
    def delete_column(self, id: str) -> None:
        """
            Отправляется PUT-запрос для удаления колонки
            :param id: str: id колонки
            :return: None
        """

        requests.put('{url}/{id}'.format(url=self.__url, id=id), headers=self.__headers, json={"deleted": True})
