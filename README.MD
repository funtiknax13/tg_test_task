# Телеграм-бот для создания задач
[Работающий проект](https://t.me/atomic_habits13_bot)

Виртуальное окружение:
```
установить виртуальное окружение:
   python -m venv venv
установить библиотеки из файла requirements.txt:
   pip install -r requirements.txt
```

Для запуска создать файл database.ini для соединения с postgresql:
```
[postgresql]
host=
user=
password=
port=
```

Для названия БД и токена ТГ создать файл .env:

```
DB_NAME=
TOKEN=
```

Файл для запуска:

- bot.py