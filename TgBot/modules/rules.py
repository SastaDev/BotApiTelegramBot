from TgBot import bot, db
from BotApiTelegram.types import Button
from BotApiTelegram import filters

@bot.on_update(filters.command('setrules'))
def on_setrules(message):
    if not message.is_group:
        message.reply('Use this in groups only.')
        return
    chat_id = message.chat.id
    user_id = message.from_user.id
    perms = bot.get_permissions(chat_id)
    if user_id == 1087968824: # @GroupAnonymousBot's ID.
        btns = [Button.inline('Tap me to verify yourself!', 'anonymous_verification_setrules')]
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
        message.reply('Write some rules text after command.')
        return
    else:
        rules_text = message.text[10:]
        db.set_rules(chat_id, rules_text)
        message.reply('Done, I have set this message for rules.')

@bot.on_update(filters.command('rules'))
def on_rules(message):
    if not message.is_group:
        message.reply('Use this in groups only.')
        return
    chat_id = message.chat.id
    rules_text = db.get_rules(chat_id)
    message.reply(rules_text)