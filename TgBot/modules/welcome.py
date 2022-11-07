from TgBot import bot, db
from BotApiTelegram.types import Button
from BotApiTelegram import filters

@bot.on_update(filters.command('setwelcome'))
def on_setwelcome(message):
    if not message.is_group:
        message.reply('Use this in groups only.')
        return
    chat_id = message.chat.id
    user_id = message.from_user.id
    perms = bot.get_permissions(chat_id)
    if user_id == 1087968824: # @GroupAnonymousBot's ID.
        btns = [Button.inline('Tap me to verify yourself!', 'anonymous_verification_setwelcome')]
        message.reply('<b>Seems like an Anonymous Admin is trying to do this.</b>\n<i>Click the button given below to verify yourself before Continuing...</i>', buttons=btns)
        return
    splited_text = message.text.split()
    if not perms.is_creator and not perms.is_admin:
        message.reply('Only admins can use this command!')
        return
    elif not perms.can_change_info:
        message.reply('You need <b>Change Group Info</b> right to do this.')
        return
    elif len(splited_text) <= 1:
        message.reply('Write some welcome message text after command.')
        return
    else:
        welcome_text = message.text[12:]
        db.set_welcome(chat_id, welcome_text)
        message.reply('Done, I have set this message for welcoming members.')

@bot.on_update(filters.command('welcome'))
def on_welcome(message):
    chat_id = message.chat.id
    welcome_text = db.get_welcome(chat_id)
    message.reply(welcome_text)

@bot.on_update(filters.chat(joined=True))
def on_new_member(message):
    if not message.is_group:
        message.reply('Use this in groups only.')
        return
    chat_id = message.chat.id
    welcome_text = db.get_welcome(chat_id)
    buttons = [
        [Button.url('Rules', 'https://telegram.dog/BotApiTelegramBot?start=rules_{}'.format(chat_id))],
        [Button.url('Updates Channel', 'https://telegram.dog/BotApiTelegram')],
        [Button.url('Examples', 'https://github.com/SastaDev/BotApiTelegram/tree/main/examples')],
        [Button.url('Documentaion', 'https://BotApiTelegram.tk')]
        ]
    message.reply(welcome_text, buttons=buttons)