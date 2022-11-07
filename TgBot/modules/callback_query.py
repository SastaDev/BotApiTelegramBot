from BotApiTelegram import filters
from BotApiTelegram.types import Button
from TgBot import bot

@bot.on_update(filters.regex(r'delete_msg'))
def on_delete_msg(callback_query):
    chat = callback_query.chat
    user = callback_query.from_user
    perms = bot.get_permissions(chat, user)
    if not perms.is_creator and not perms.is_admin:
        callback_query.answer('Only admins can use this command!', show_alert=True)
        return
    if not perms.can_delete_messages:
        callback_query.answer('You need "can delete messages" to do this.')
        return
    callback_query.delete()
    callback_query.answer('• Successfully Deleted Message!')

@bot.on_update(filters.regex(r'unban_(.+)'))
def on_unban(callback_query):
    user_to_unban = callback_query.pattern_match.group(1)
    user_to_unban = bot.get_chat(user_to_unban)
    chat = callback_query.chat
    user = callback_query.from_user
    perms = bot.get_permissions(chat, user)
    if not perms.is_creator and not perms.is_admin:
        callback_query.answer('Only admins can use this command!', show_alert=True)
        return
    elif not perms.can_ban:
        callback_query.answer('You need <b>Ban User</b> right to do this.', show_alert=True)
        return
    try:
        bot.unban_user(chat, user_to_unban)
    except Exception as e:
        text = 'ERROR: {}'.format(e)
        callback_query.answerr(text)
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
    text = '''
<b>UnBanned:</b> {}
<b>UnBanned By:</b> {}
    '''.format(unbanned, unbanned_by)
    buttons = [
        [Button.inline('Ban', 'ban_{}'.format(user_to_unban.id))],
        [Button.inline('Delete', 'delete_msg')]
        ]
    callback_query.edit(text, buttons=buttons)
    callback_query.answer('Successfully Un-Banned!')

@bot.on_update(filters.regex(r'ban_(.+)'))
def on_ban(callback_query):
    user_to_ban = callback_query.pattern_match.group(1)
    user_to_ban = bot.get_chat(user_to_ban)
    chat = callback_query.chat
    user = callback_query.from_user
    perms = bot.get_permissions(chat, user)
    if not perms.is_creator and not perms.is_admin:
        callback_query.answer('Only admins can use this command!', show_alert=True)
        return
    elif not perms.can_ban:
        callback_query.answer('You need <b>Ban User</b> right to do this.', show_alert=True)
        return
    try:
        bot.ban_user(chat, user_to_ban)
    except Exception as e:
        text = 'ERROR: {}'.format(e)
        callback_query.reply(text)
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
    text = '''
<b>Banned:</b> {}
<b>Banned By:</b> {}
    '''.format(banned, banned_by)
    buttons = [
        [Button.inline('UnBan', 'unban_{}'.format(user_to_ban.id))],
        [Button.inline('Delete', 'delete_msg')]
        ]
    callback_query.edit(text, buttons=buttons)
    callback_query.answer('Successfully Banned!')