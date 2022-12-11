import os

from dotenv import load_dotenv

load_dotenv()
api_id = os.getenv('TG_ID')
api_hash = os.getenv('TG_HASH')
DATABASE_URL = os.getenv('DB_URL')
DEEPL = os.environ['DEEPL']

CHANNEL_NEWS = -1001839268196
CHANNEL_BACKUP = -1001861018052
CHANNEL_SOURCE = -1001616523535
CHANNEL_INFO = -1001825780867
CHANNEL_MEME = -1001482614635
