from BotApiTelegram import filters
from BotApiTelegram.types import Button
from TgBot import bot
from . import helpers
import re

@bot.on_update(filters.command('ban'))
def on_ban(message):
    if not message.is_group:
        message.reply('Use this in groups only.')
        return
    user = message.from_user
    chat = message.chat
    user_to_ban = helpers.getID(message)
    if user_to_ban is None:
        message.reply('You did not mentioned whom to ban.')
        return
    elif user_to_ban is False:
        message.reply('I could not able to find this user...')
        return
    if user.id == 1087968824: # @GroupAnonymousBot's ID.
        btns = [Button.inline('Tap me to verify yourself!', 'anonymous_verification_ban_{}'.format(user_to_ban))]
        message.reply('<b>Seems like an Anonymous Admin is trying to do this.</b>\n<i>Click the button given below to verify yourself before Continuing...</i>', buttons=btns)
        return
    user_to_ban = bot.get_chat(user_to_ban)
    perms = bot.get_permissions(chat, user)
    if not perms.is_creator and not perms.is_admin:
        message.reply('Only admins can use this command!')
        return
    elif not perms.can_ban:
        message.reply('You need <b>Ban User</b> right to do this.')
        return
    try:
        bot.ban_user(chat, user_to_ban)
    except Exception as e:
        text = '<b>An error occurred while banning:</b>\n\n<b>ERROR:</b> {}'.format(e)
        message.reply(text)
        return
    banned = '<a href="tg://user?id={}">{}'.format(user_to_ban.id, user_to_ban.first_name)
    if user_to_ban.last_name:
        banned += ' {}'.format(user_to_ban.last_name)
    banned += '</a>'
    banned_by = '<a href="tg://user?id={}">{}'.format(user.id, user.first_name)
    if user.last_name:
        banned_by += ' {}'.format(user.last_name)
    banned_by += '</a>'
    banned_by += ' ({})'.format('Owner' if perms.is_creator else 'Admin')
    splited_text = message.text.split()
    if message.is_reply and len(splited_text) >= 2: # reply ban.
        regex = re.search('(.+) (.+)', message.text, re.DOTALL)
        reason = regex.group(2)
        reason = '<code>' + reason + '</code>'
    elif len(splited_text) >= 3: # mention ban.
        regex = re.search('(.+) (.+) (.+)', message.text, re.DOTALL)
        reason = regex.group(3)
        reason = '<code>' + reason + '</code>'
    else:
        reason = '<i>No reason specified.</i>'
    text = '''
<b>Banned:</b> {}
<b>Banned By:</b> {}
<b>Reason:</b> {}
    '''.format(banned, banned_by, reason)
    buttons = [
        [Button.inline('UnBan', 'unban_{}'.format(user_to_ban.id))],
        [Button.inline('Delete', 'delete_msg')]
        ]
    message.reply(text, buttons=buttons)