<p align="center">
    <img alt="logo" src="Other%20Services/Web/images/img.png" width="400px">
</p>
<h1 align='center'>LinkHouse</h1>
<p align='center'>
  <strong>Команда БЕЗУМЦЫ</strong><br>
  IT INNO HACK 2024<br>
  Кейс №1 "Record Linkage для данных о клиентах"
</p>

---

## Структура проекта


## Инструкция по использованию
### Разворачивание системы
1. Перейдите в папку `Docker`, здесь хранятся файлы самого решения для запуска. Выполняйте все последующие инструкции, находясь в ней.
2. Создайте файл `.env` с переменными окружения, по примеру в `.env_example`
```dotenv
CLICKHOUSE_DB=default
CLICKHOUSE_USER=default
CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT=1
CLICKHOUSE_PASSWORD=

CLICKHOUSE_HOST=clickhouse
CLICKHOUSE_PORT=8123

PROCESSING_LIMIT=8000000
```
3. Перенесите .csv файлы в папку `input_data`.
4. Запустите Docker Compose: `docker compose up --build`.
5. Скрипт сразу начнет свою работу, в логах можете наблюдать за его работой.
