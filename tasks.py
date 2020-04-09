from gathering.gathering_posts import TelegramPostCollector


async def gather_posts(channel_addr,finish_date_time):
    telegram_collector = None
    try:
        telegram_collector = TelegramPostCollector(finish_date_time=finish_date_time)
        await telegram_collector.collect_posts(channel_addr)
    except Exception as e:
        print("exception in tasks.py:gather_posts", e)
        raise e
    finally:
        if telegram_collector is not None:
            telegram_collector.close_client_session()