from TgBot import bot, db
from BotApiTelegram.types import Button
from BotApiTelegram import filters

@bot.on_update(filters.command('setwelcome'))
def on_setwelcome(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    admins = bot.getAdmins(chat_id)
    splited_text = message.text.split()
    if user_id not in [x.user.id for x in admins]:
        message.reply('Only admins can use this command!')
        return
    elif len(splited_text) <= 1:
        message.reply('Write some welcome message text after command.')
        return
    else:
        welcome_text = message.text[12:]
        db.set_welcome(chat_id, welcome_text)
        message.reply('Done, I have set this message for welcoming members.')

@bot.on_update(filters.chat(joined=True))
def on_new_member(message):
    chat_id = message.chat.id
    welcome_text = db.get_welcome(chat_id)
    buttons = [
        [Button.url('Updates Channel', 'https://telegram.dog/BotApiTelegram')],
        [Button.url('Examples', 'https://github.com/SastaDev/BotApiTelegram/tree/main/examples')],
        [Button.url('Documentaion', 'https://BotApiTelegram.tk')]
        ]
    message.reply(welcome_text, buttons=buttons)