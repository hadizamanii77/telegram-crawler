import asyncio

from celery import Celery
from gathering.gathering_posts import TelegramPostCollector

app = Celery('tasks', broker='amqp://guest@localhost//',backend='amqp',)


@app.task
def gather_posts(list_of_channels):
    loop = asyncio.get_event_loop()
    for channel in list_of_channels:
        print("channel {} start fetching".format(channel))
        telegram_collector = TelegramPostCollector()
        loop.run_until_complete(telegram_collector.collect_posts(channel))
