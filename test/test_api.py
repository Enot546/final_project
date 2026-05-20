import allure
import random
from api_client.AuhtApi import AuthApi
from api_client.ProjectApi import ProjectApi
from api_client.BoardApi import BoardApi
from api_client.ColumnApi import ColumnApi
from testdata.DataProvider import DataProvider


@allure.epic('Тестирование функционала REST API сервиса YouGile')
@allure.severity(allure.severity_level.BLOCKER)
@allure.suite('API-тесты по управлению проектами и колонками')
class TestAPI:

    @allure.story('Позитивные проверки по управлению проектами')
    @allure.title('Добавление проекта компании')
    @allure.description('Добавление нового проекта в компанию')
    @allure.feature('CREATE')
    def test_create_project(
        self,
        project_api: ProjectApi,
        test_data: DataProvider,
        delete_utility_project: dict,
    ):
        with allure.step('Сгенерировать уникальное название проекта'):
            project_title = test_data.get('project_title') + str(random.randint(0, 99999))

        with allure.step('Получить количество проектов ДО'):
            len_before = len(project_api.get_projects().json()['content'])

        with allure.step('Отправить API-запрос для создания проекта "{project_title}"'):
            api_response = project_api.create_project(project_title)

        with allure.step('Запросить информацию по новому проекту'):
            new_project = project_api.get_project_by_id(api_response.json()['id']).json()

        with allure.step('Получить количество проектов ПОСЛЕ'):
            len_after = len(project_api.get_projects().json()['content'])

        delete_utility_project['project_id'] = api_response.json()['id']

        with allure.step('Проверка:'):
            with allure.step('Статус-код 201'):
                assert api_response.status_code == 201
            with allure.step('В ответе вернулся id нового проекта'):
                assert api_response.json().get('id', None) != None
            with allure.step('Название нового проекта корректно сохранено'):
                assert new_project['title'] == project_title
            with allure.step('Количество проекто стало +1'):
                assert len_after - len_before == 1

    @allure.story('Позитивные проверки по управлению проектами')
    @allure.title('Получение списка актуальных проектов')
    @allure.description('Получить список актуальных проектов компании, у которых нет атрибута deleted:true')
    @allure.feature('GET')
    def test_get_active_project(
        self,
        project_api: ProjectApi,
        generate_random_str: str,
        delete_utility_project: dict
    ):
        actual_project_id = project_api.create_project(f'1. {generate_random_str}').json()['id']
        deleted_project_id = project_api.create_project(f'1. {generate_random_str}').json()['id']

        project_api.delete_project(deleted_project_id)

        api_response = project_api.get_projects()

        with allure.step('Создать список id проектов, полученных в запросе'):
            api_ids = []
            for proj in api_response.json()['content']:
                api_ids.append(proj['id'])

        delete_utility_project['project_id'] = actual_project_id

        with allure.step('Проверка:'):
            with allure.step('Статус-код 200'):
                assert api_response.status_code == 200
            with allure.step('Список id проектов, полученных в запросе, НЕ содрежит id удаленного проекта'):
                assert not deleted_project_id in api_ids
            with allure.step('Список id проектов, полученных в запросе, содрежит id актуального проекта'):
                assert actual_project_id in api_ids

    @allure.story('Позитивные проверки по управлению колонками')
    @allure.title('Редактирование колонки')
    @allure.description('Изменить атрибуты колонки - название, цвет, родительскую доску')
    @allure.feature('PUT')
    def test_update_column(
        project_api: ProjectApi,
        board_api: BoardApi,
        column_api: ColumnApi,
        create_utility_project: dict,
        delete_utility_project: dict,
        delete_utility_board: dict,
        delete_utility_column: dict,
        test_data: DataProvider,
        generate_random_str: str
    ):
        project_id = create_utility_project['project_id']
        with allure.step('Добавить в проект доски'):
            with allure.step('Первая доска "1 {generate_random_str}"'):
                first_board_id = board_api.create_board(f'1 {generate_random_str}', project_id).json()['id']
            with allure.step('Вторая доска "2 {generate_random_str}"'):
                second_board_id = board_api.create_board(f'2 {generate_random_str}', project_id).json()['id']

        with allure.step('Добавить колонку на перую доску'):
            column_id = column_api.create_column(f'Колонка {generate_random_str}', first_board_id).json()['id']

        body = {
            'title': test_data.get('new_column_title'),
            'color': test_data.get('new_column_color'),
            'boardId': second_board_id
        }
        api_response = column_api.update_column(column_id, body)

        updated_column = column_api.get_column_by_id(column_id).json()

        delete_utility_project['project_id'] = project_id
        delete_utility_board['first_board_id'] = first_board_id
        delete_utility_board['second_board_id'] = second_board_id
        delete_utility_column['column_id'] = column_id

        with allure.step('Проверка:'):
            with allure.step('Статус-код 200'):
                assert api_response.status_code == 200
            with allure.step('В ответе вернулся id редактируемой колонки'):
                assert api_response.json()['id'] == column_id
            with allure.step('Название колонки обновлено'):
                assert test_data.get('new_column_title') in updated_column['title']
            with allure.step('Цвет колонки обновлен'):
                assert test_data.get_int('new_column_color') == updated_column['color']
            with allure.step('Родительская доска колонки обновлена'):
                assert second_board_id == updated_column['boardId']

    @allure.story('Негативные проверки по управлению проектами')
    @allure.title('Добавление проекта с пустой строкой в названии')
    @allure.description('Проверка обработки запроса на добавление проекта с пустой строкой в названии')
    @allure.feature('GET')
    def test_create_project_empty_title(self, project_api: ProjectApi, test_data: DataProvider):
        with allure.step('Получить количество проектов ДО'):
            len_before = len(project_api.get_projects().json()['content'])

        api_response = project_api.create_project('')

        with allure.step('Получить количество проектов ПОСЛЕ'):
            len_after = len(project_api.get_projects().json()['content'])

        error_msg = test_data.get('error_description_empty_project_title')
        with allure.step('Проверка:'):
            with allure.step('Статус-код 400'):
                assert api_response.status_code == 400
            with allure.step('В ответе пришло поле statusCode:400'):
                assert api_response.json()['statusCode'] == 400
            with allure.step('В ответе поле message содержит описание ошибки'):
                assert error_msg in api_response.json()['message']
            with allure.step('В ответе пришло поле error:Bad Request'):
                assert test_data.get('error_bad_request') == api_response.json()['error']
            with allure.step('Количество проектов не изменилось'):
                assert len_before == len_after

    @allure.story('Негативные проверки по управлению проектами')
    @allure.title('Добавление проекта с удаленном ключом API')
    @allure.description('Проверка обработки запроса на добавление проекта с удаленном ключом API')
    @allure.feature('POST')
    def test_create_project_deleted_api_key(
        self,
        auth_api: AuthApi,
        project_api: ProjectApi,
        test_data: DataProvider
    ):
        with allure.step('Получить количество проектов ДО'):
            len_before = len(project_api.get_projects().json()['content'])

        key_resp = auth_api.create_api_key(test_data.get('company_id'))
        key = key_resp.json()['key']
        auth_api.delete_api_key(key)
        auth_api.get_api_keys(test_data.get('company_id'))

        api_response = project_api.create_project('test', key)

        with allure.step('Получить количество проектов ПОСЛЕ'):
            len_after = len(project_api.get_projects().json()['content'])

        error_msg = test_data.get('error_description_unauth')
        error = test_data.get('error_unauth')

        with allure.step('Проверка:'):
            with allure.step('Статус-код 401'):
                assert api_response.status_code == 401
            with allure.step('В ответе пришло поле statusCode:401'):
                assert api_response.json()['statusCode'] == 401
            with allure.step('В ответе пришло поле message:{error_msg}'):
                assert error_msg == api_response.json()['message']
            with allure.step('В ответе пришло поле error:{error}'):
                assert error == api_response.json()['error']
            with allure.step('Количество проектов не изменилось'):
                assert len_before == len_after
