from dotenv import load_dotenv
import os

#загрузка переменных окружения
load_dotenv()

TG_BOT_TOKEN=os.getenv('TG_BOT_TOKEN', '')
SQLALCHEMY_DB_URL= os.getenv('SQLALCHEMY_DB_URL', '')