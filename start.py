from gathering.gathering_posts import TelegramPostCollector
import asyncio
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    channels = []
    with open('channels.txt') as file:
        for line in file.readlines():
            channels.append(line)
    telegram_collector = TelegramPostCollector()
    loop.run_until_complete(telegram_collector.collect_posts(channels))