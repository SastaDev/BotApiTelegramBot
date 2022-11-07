from TgBot import bot
from BotApiTelegram import types, tools

def getID(message):
    ID = None
    splited_text = message.text.split()
    if message.is_reply:
        ID = message.reply_to_message.from_user.id
    elif len(splited_text) >= 2:
        user = splited_text[1]
        if user[0] == '@':
            try:
                chat = bot.get_chat(user)
                if isinstance(chat, types.Chat):
                    ID = chat.id
                elif isinstance(chat, types.User):
                    ID = chat.user_id
            except:
                ID = False
        entities = tools.parse_entities(message.msg)
        if entities[1]:
            user = entities[1][0]
            ID = user.id
        elif str(user).isdigit():
            try:
                chat = bot.get_chat(user)
                ID = chat.id
            except:
                ID = False
    else:
        ID = None
    return ID