#run.sh
results=./allure_files
rep_history=./allure_report/history
report=./allure_report

rm -rf $results # Удалить папку с результатами
python3 -m pytest --alluredir=$results # Запустить UI + API автотестытесты 
# python3 -m pytest test/test_ui.py::UITest --alluredir=$results # Запустить UI-автотестытесты 
# python3 -m pytest test/test_api.py::APITest --alluredir=$results # Запустить API-автотестытесты 
mv $rep_history $results # Перенести историю в результаты 
rm -rf $report # Удалить отчет
allure generate $results -o $report # Сгенерировать отчет
allure open $report # Открыть отчет