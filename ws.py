from datetime import datetime
from quart import Quart, request, websocket
from tasks import gather_posts

app = Quart(__name__)


@app.websocket('/ws/gather/posts')
async def gather_posts_api():
    while True:
        try:
            channel_addr = await websocket.receive()
            await websocket.send(
                "please enter date (YYYY-MM-DD) : today is {}".format(str(datetime.date(datetime.now()))).format(
                    channel_addr))
            finish_date_time = await websocket.receive()
            await websocket.send("start fetching {} channel".format(channel_addr))
            await gather_posts(channel_addr,finish_date_time)
            await websocket.send("finish fetching {} channel".format(channel_addr))
            await websocket.send(
                "address : http://194.5.192.130/telegram_files/{date}/{channel_addr}.csv".format(
                    date=str(datetime.date(datetime.now())),
                    channel_addr=channel_addr.split('/')[-1]))  # this address should get from MessageSaver in next version
        except Exception as e:
            print(e)
            websocket.send(
                "exist one exception"
            )