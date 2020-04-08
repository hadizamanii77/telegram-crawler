from gathering.gathering_posts import TelegramPostCollector


async def gather_posts(list_of_channels):
    for channel in list_of_channels:
        print("channel {} start fetching".format(channel))
        telegram_collector = TelegramPostCollector()
        await telegram_collector.collect_posts(channel)