import configparser
from pathlib import Path


# Absolut path
dir_path = Path.cwd()
# path = Path(dir_path, 'config.ini')
path = Path(dir_path, 'bot/config.ini')
config = configparser.ConfigParser()
config.read(path)

# Constants
DB_URL = config['SQL']['db_url']
API_ID = config['Telegram']['api_id']
API_HASH = config['Telegram']['api_hash']

# Имена сессий (сессии должни принадлежать одному аккаунту)
MY_ACCOUNT = "my_account"
MY_ACCOUNT_2 = "my_account_2"

# Слова триггеры для остановки воронки
TRIGGERS_FOR_FINISHED = ["прекрасно", "ожидать"]

# Слово триггер для пропуска msg_2 (согласно ТЗ)
TRIGGER_FOR_MISS_MSG = "купить"

# Лимит сообщений для анализа слов триггеров из диалога с клиентом
MSG_HISTORY_LIMIT = 100

# Время ожидания перед отправкой следующего сообщения(в секундах)
WAIT_TIME_1 = 6*60
WAIT_TIME_2 = 39*60
WAIT_TIME_3 = 60*26*60

# Время через которое проверяется отправка сообщений (в секундах)
CHECK_TIME = 30

# Вывод параметров для steps при триггере и ошибках
FINISHED = -1
USER_ERROR = -2
