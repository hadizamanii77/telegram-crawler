from datetime import datetime
from quart import Quart, request, websocket
from tasks import gather_posts

app = Quart(__name__)


@app.websocket('/ws/gather/posts')
async def gather_posts_api():
    try:
        channel_addr_list = []
        while True:
            channel_addr = await websocket.receive()
            if channel_addr == 'q':
                break
            channel_addr_list.append(channel_addr)

        await websocket.send(
            "please enter date (YYYY-MM-DD) : today is {}".format(str(datetime.date(datetime.now()))).format(
                channel_addr))
        finish_date_time = await websocket.receive()
        await websocket.send("start fetching channels")
        result = await gather_posts(channel_addr_list, finish_date_time)
        await websocket.send("finish fetching channels")
        await websocket.send(str(result))
    except Exception as e:
        print(e)
        await websocket.send(
            "exist one exception"
        )
