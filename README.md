# yougile_automation

## Проект по автоматизации API и UI тестирования на python для Yougile
[Сервис “Yougile”](https://ru.yougile.com) позволяет планировать и управлять задачами в компании.
Для проекта был выбран функционал, доступный в веб-интерфейсе и через REST API.
Составлено 5 UI- и 5 API-автотестов, для формирования отчета о проведенных автотестах используется инструмент Allure.

### Шаги
1. Склонировать проект `git clone https://github.com/Enot546/final_project.git`
2. Установить зависимости
3. Запустить тесты с указанием пути к дирректории результатов тестирования `pytest --alluredir allure_files`
4. Сформировать отчет `allure generate allure_files -o allure_report`
5. Открыть отчет `allure open allure_report`

### Стек:
- pytest
- selenium
- requests
- allure
- config


### Тестовые данные
Файл с тестовыми данными (test_data.json):
- содержит данные для авторизации
    - при смене пользователя необходимо воспользоваться API-документацией Yougile  и обновить значения в полях:
        - email, password, company, user_name, company_id, api_key
- названия ключей в файле менять нельзя
- значения текстовых данных для названий (ключ *title*) можно задавать любые

### Настройки окружения
Файл с переменными окружения (config.ini) содержит:
- базовый url-адрес для API-запросов
- базовый url-адрес для веб-интерфейса
- название браузера для проведения UI-автотестов
- timeout для настройки браузера

### Полезные ссылки
- [Проект “Yougile”: тест план + отчет о тестировании](https://redtest.yonote.ru/share/7cac2222-ab07-4f8c-87d9-be9774f8353d)
- [Веб-интерфейс сервиса Yougile](https://ru.yougile.com/)

### Библиотеки
- pip3 install pytest
- pip3 install selenium
- pip3 install webdriver-manager
- pip3 install allure-pytest
- pip3 install requests

### Запуск тестов
- `pytest` | `python3 -m pytest`  (запуск тестов)
- `python3 -m pytest -s` (вывод в консоль print)
- `python3 -m pytest -v` (запуск тестов с подробным выводом в консоль)
- `python3 -m pytest filename.py` (запуск тестов из файла)
- `python3 -m pytest filename.py::Class::function:` (запуск тестов по идентификатрам узлов)
- `python3 -m pytest --alluredir allure_files` (запуск тестов и сохранение отчета о результатах тестирования)
- `sh run.sh` (запуск тестов с сохранением истории прогонов и генерация отчета с результатами тестирования)