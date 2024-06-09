
# Smedia Telegram Bot (TEST TASK)

Бот для Telegram, который автоматически отправляет сообщения пользователям в зависимости от времени и наличия триггерных слов.

# Описание работы

1. Получаем первое сообщение от пользователя и регистрируем его в базе данных.
2. Через 6 минут отправляем Текст1, если не найдены триггерные слова остановки от юзербота.
3. Через 39 минут проверяем триггерные слова пропуска сообщения отюзербота. Так же проверяем на триггерные слова остановки от юзербота. Если триггер не найден - отправляем Текст2. 
4. Через 1 день и 2 часа отправляем Текст3, если триггер остановки не был найден.
5. Если найдено слово "прекрасно" или "ожидать", процесс останавливается и статус меняется на finished.


## Структура проекта

````
smedia_tt/
├── bot/
│   ├── init.py
│   ├── config.ini
│   ├── config.py
│   ├── db.py
│   ├── main.py
│   ├── models.py
│   ├── scheduler.py
├── venv/
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
````

# Значения step (в БД)
- step = -1: остановка по слову триггеру.     
- step = -2: пользователь заблокировал бота, деактивировал аккаунт или ID некорректен.



## Установка и запуск

1. Склонируйте репозиторий:
    ```sh
    git clone https://github.com/artdmsav/smedia_bot.git
    cd smedia_bot
    ```

2. Замените данные с Вашими настройками в файле `bot/config.ini`:
    ```ini
    [SQL]
    db_url = postgresql+asyncpg://admin:password@db:5432/smedia_db

    [Telegram]
    api_id = your_api_id
    api_hash = your_api_hash
    ```
3. Создайте или добавьте две сессии одного аккаунта в папку `bot`. 
4. Замените название сессий на название ваших сессий в папке `config.py`
```python
# Имена сессий (сессии должни принадлежать одному аккаунту)
MY_ACCOUNT = "my_account"
MY_ACCOUNT_2 = "my_account_2"
```
5. Постройте и запустите контейнеры с помощью Docker Compose:
    ```sh
    docker-compose up --build
    ```

## Сервисы

- **db**: Сервис PostgreSQL для хранения данных.
- **models**: Сервис для инициализации базы данных и создания таблиц.
- **main**: Основное приложение Telegram бота.
- **scheduler_bot**: Планировщик для автоматической отправки сообщений.

## Использование

- Контейнер `init_db` выполняется один раз для инициализации базы данных.
- Контейнеры `main_bot` и `scheduler_bot` работают в фоновом режиме для постоянного взаимодействия с пользователями и отправки сообщений.

## Остановка

Для остановки всех сервисов выполните:
```sh
docker-compose down
```

# ТЗ от заказчика

![Снимок экрана 2024-06-06 в 2.39.44 PM.png](..%2F..%2FDesktop%2F%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202024-06-06%20%D0%B2%202.39.44%E2%80%AFPM.png)



