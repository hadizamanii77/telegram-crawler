import asyncio

from global_utils.connect import TelegramConnection
from global_utils.save import MessageSaver
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (PeerChannel)


class TelegramPostCollector:
    def __init__(self,finish_date_time = None):
        self.limit = 100
        self.total_count_limit = 1000
        self.telegram_connection = TelegramConnection()
        self.client = None
        self.finish_date_time = finish_date_time

    async def get_client(self):
        return await self.telegram_connection.get_client()

    async def close_client(self):
        await self.client.session.close()

    async def get_channel(self, channel_identifier):
        if channel_identifier.isdigit():
            entity = PeerChannel(int(channel_identifier))
        else:
            entity = channel_identifier
        channel = await self.client.get_entity(entity)
        return channel

    async def collect_posts(self, channel_identifier):
        self.client = await self.get_client()
        message_saver = MessageSaver(channel_identifier)
        channel = await self.get_channel(channel_identifier)
        offset_id = 0
        total_message = 0
        while True:
            history = await (
                self.client(
                    GetHistoryRequest(
                        peer=channel,
                        offset_id=offset_id,
                        offset_date=None,
                        add_offset=0,
                        limit=100,
                        max_id=0,
                        min_id=0,
                        hash=0
                    )
                )
            )
            if not history.messages or len(history.messages) == 0:
                break
            messages = history.messages
            offset_id = messages[len(messages) - 1].id
            total_message += len(messages)
            print("{} message fetched.".format(total_message))
            message_saver.save_messages(messages,self.finish_date_time)
            if total_message >= self.total_count_limit:
                break
        await self.close_client_session()
