import pymongo
import dns

dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

class MongoDB:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.mongo_client = pymongo.MongoClient(connection_string)

    def set_welcome(self, chat_id, text):
        d = self.mongo_client['BotApiTelegramDB']
        col = d['welcomes']
        data = {
            'chat_id': chat_id,
            'text': str(text)
        }
        col.update_one({'_id': 'welcomes'},
        {'$set': data}, upsert=True)

    def get_welcome(self, chat_id):
        d = self.mongo_client['BotApiTelegramDB']
        col = d['welcomes']
        l = list(col.find({'chat_id': chat_id}))
        if l:
            return l[0].get('text')
        else:
            return None

    def set_rules(self, chat_id, text):
        d = self.mongo_client['BotApiTelegramDB']
        col = d['rules']
        data = {
            '_id': 'rules',
            'chat_id': chat_id,
            'text': str(text)
        }
        col.update_one({'_id': 'rules'},
        {'$set': data}, upsert=True)

    def get_rules(self, chat_id):
        d = self.mongo_client['BotApiTelegramDB']
        col = d['rules']
        l = list(col.find({'chat_id': chat_id}))
        if l:
            return l[0].get('text')
        else:
            return None