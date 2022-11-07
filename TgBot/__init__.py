from BotApiTelegram import TelegramBot
from . import database
import json 

def config():
    return json.loads(open('config.json').read())

BOT_TOKEN = config()['BOT_TOKEN']
MONGODB_URI = config()['MONGODB_URI']

bot = TelegramBot('bot_db', bot_token=BOT_TOKEN)

bot.default_settings.parse_mode = 'html'

db = database.MongoDB(MONGODB_URI)

from . import modules