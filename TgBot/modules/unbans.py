from BotApiTelegram import filters
from BotApiTelegram.types import Button
from TgBot import bot
from . import helpers
import re

@bot.on_update(filters.command('unban'))
def on_unban(message):
    user = message.from_user
    chat = message.chat
    user_to_unban = helpers.getID(message)
    if user_to_unban is None:
        message.reply('You did not mentioned whom to unban.')
        return
    elif user_to_unban is False:
        message.reply('I could not able to find this user...')
        return
    user_to_unban = bot.get_chat(user_to_unban)
    perms = bot.get_permissions(chat, user)
    if not perms.is_creator and not perms.is_admin:
        message.reply('Only admins can use this command!')
        return
    elif not perms.can_unban:
        message.reply('You need <b>Ban User</b> right to do this.')
        return
    try:
        bot.unban_user(chat, user_to_unban)
    except Exception as e:
        text = '<b>An error occurred while unbanning:</b>\n\n<b>ERROR:</b> {}'.format(e)
        message.reply(text)
        return
    unbanned = '<a href="tg://user?id={}">{}'.format(user_to_unban.id, user_to_unban.first_name)
    if user_to_unban.last_name:
        unbanned += ' {}'.format(user_to_unban.last_name)
    unbanned += '</a>'
    unbanned_by = '<a href="tg://user?id={}">{}'.format(user.id, user.first_name)
    if user.last_name:
        unbanned_by += ' {}'.format(user.last_name)
    unbanned_by += '</a>'
    unbanned_by += ' ({})'.format('Owner' if perms.is_creator else 'Admin')
    splited_text = message.text.split()
    if message.is_reply and len(splited_text) >= 2: # reply unban.
        regex = re.search('(.+) (.+)', message.text, re.DOTALL)
        reason = regex.group(2)
        reason = '<code>' + reason + '</code>'
    elif len(splited_text) >= 3: # mention unban.
        regex = re.search('(.+) (.+) (.+)', message.text, re.DOTALL)
        reason = regex.group(3)
        reason = '<code>' + reason + '</code>'
    else:
        reason = '<i>No reason specified.</i>'
    text = '''
<b>UnBanned:</b> {}
<b>UnBanned By:</b> {}
<b>Reason:</b> {}
    '''.format(unbanned, unbanned_by, reason)
    buttons = [
        [Button.inline('Ban', 'ban_{}'.format(user_to_unban.id))],
        [Button.inline('Delete', 'delete_msg')]
        ]
    message.reply(text, buttons=buttons)