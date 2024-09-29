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

## Ограничения!!
Docker Desktop по умолчанию имеет лимиты для используемой оперативной памяти и дискового пространства. Это можно проверить в Docker Desktop по пути `Settings > Resources`
Рекомендуемые настройки:
Memory Limit: 12 GB
Virtual Disk Limit: 48 GB

В зависимости от Memory Limit потом измените переменную в `.env` дальше по принципу:
8 GB -> PROCESSING_LIMIT=6000000
10 GB -> PROCESSING_LIMIT=8000000
12 GB -> PROCESSING_LIMIT=10000000

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
Из данных переменных по-хорошему можно ничего не менять, кроме переменной `PROCESSING_LIMIT`. Всё зависит от количества оперативной памяти на машине. Обращайтесь к пункту "Ограничения", чтобы узнать значение
3. Перенесите .csv файлы в папку `input_data` с названиями `main1.csv`, `main2.csv`, `main3.csv`.
4. Запустите Docker Compose: `docker compose up --build`.
5. Скрипт сразу начнет свою работу, в логах можете наблюдать за его работой.
6. ClickHouse будет первое время инициализироваться, после галочки в логах перейдите на `127.0.0.1:8123/play` и смотрите данные через `SELECT * FROM table_results LIMIT 100 OFFSET 0` и т.д.
