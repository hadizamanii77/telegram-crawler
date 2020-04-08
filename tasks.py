from gathering.gathering_posts import TelegramPostCollector


async def gather_posts(channel_addr,finish_date_time):
    telegram_collector = TelegramPostCollector(finish_date_time=finish_date_time)
    await telegram_collector.collect_posts(channel_addr)