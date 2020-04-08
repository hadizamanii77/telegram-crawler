from gathering.gathering_posts import TelegramPostCollector


async def gather_posts(channel_addr):
    telegram_collector = TelegramPostCollector()
    await telegram_collector.collect_posts(channel_addr)