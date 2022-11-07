from TgBot import bot, db
from BotApiTelegram.types import Button
from BotApiTelegram import filters

@bot.on_update(filters.regex('^/start$'))
def on_start(message):
    text = '''
Hello, I'm a bot which was created by using @BotApiTelegram python library.

I was made to manage chat @BotApiTelegramChat and i am an examples of this library.
    '''
    buttons = [
        [Button.url('Bot Api Telegram', 'https://telegram.dog/BotApiTelegramChat')],
        [Button.url('Examples', 'https://github.com/SastaDev/BotApiTelegram/tree/main/examples')],
        [Button.url('Bot Source Code', 'https://github.com/SastaDev/BotApiTelegramBot')]
        ]
    message.reply(text, buttons=buttons)