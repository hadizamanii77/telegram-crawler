import asyncio
import configparser
import json

from telethon import TelegramClient


class TelegramConnection:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini")

        self.api_id = config['Telegram']['api_id']
        self.api_hash = str(config['Telegram']['api_hash'])

        self.phone = config['Telegram']['phone']
        self.username = config['Telegram']['username']

    def set_credtional(self, api_id, api_hash, phone, username):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.username = username

    async def get_client(self):
        try:
            client = TelegramClient(self.username, api_id=self.api_id, api_hash=self.api_hash)
            await client.start()
            return client
        except Exception as e:
            print(e)
            return None
