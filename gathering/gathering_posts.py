import datetime

from global_utils.connect import TelegramConnection
from global_utils.save import MessageSaver
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (PeerChannel)

today = str(datetime.datetime.now())[:10]


class TelegramPostCollector:
    def __init__(self,finish_date_time=today):
        self.limit = 100
        self.telegram_connection = TelegramConnection()
        self.client = None
        self.finish_date_time = finish_date_time

    async def get_client(self):
        return await self.telegram_connection.get_client()

    def close_client_session(self):
        self.client.session.close()

    async def get_channel(self, channel_identifier):
        if channel_identifier.isdigit():
            entity = PeerChannel(int(channel_identifier))
        else:
            entity = channel_identifier
        channel = await self.client.get_entity(entity)
        return channel

    async def collect_posts(self,channel_identifier_list):
        result = []
        url = "http://194.5.192.130/telegram_files/{date}/{channel_addr}.csv"
        for channel_identifier in channel_identifier_list:
            success = await self._collect_post(channel_identifier)
            if success:
                result.append(url.format(
                        date=str(datetime.datetime.date(datetime.datetime.now())),
                        channel_addr=channel_identifier.split('/')[
                            -1]))
        return result

    async def _collect_post(self, channel_identifier):
        try:
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
                messages_before_finish_datetime = []
                finish = False
                for message in messages:
                    if self.finish_date_time is not None and str(message.date)[
                                                        :10] >= self.finish_date_time:  # it should go to upper layer
                        messages_before_finish_datetime.append(message)
                    else:
                        finish = True
                        break
                message_saver.save_messages(messages_before_finish_datetime)
                if finish:
                    return True
        except Exception as e:
            print(e)
            return False
