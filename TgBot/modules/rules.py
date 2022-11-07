from TgBot import bot, db
from BotApiTelegram import filters

@bot.on_update(filters.command('setrules'))
def on_setrules(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    admins = bot.getAdmins(chat_id)
    splited_text = message.text.split()
    if user_id not in [x.user.id for x in admins]:
        message.reply('Only admins can use this command!')
        return
    elif len(splited_text) <= 1:
        message.reply('Write some rules text after command.')
        return
    else:
        rules_text = message.text[10:]
        db.set_rules(chat_id, rules_text)
        message.reply('Done, I have set this message for rules.')

@bot.on_update(filters.command('rules'))
def on_rules(message):
    chat_id = message.chat.id
    rules_text = db.get_rules(chat_id)
    message.reply(rules_text)