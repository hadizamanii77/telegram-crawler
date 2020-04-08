import asyncio

from celery import Celery
from gathering.gathering_posts import TelegramPostCollector

app = Celery('tasks', broker='amqp://guest@localhost//',backend='amqp',)


@app.task
def gather_posts(list_of_channels):
    for channel in list_of_channels:
        print("channel {} start fetching".format(channel))
        telegram_collector = TelegramPostCollector()
        telegram_collector.collect_posts(channel)
