from quart import Quart
from quart import request
from tasks import gather_posts

app = Quart(__name__)


@app.route('/api/gather/posts', methods=['POST'])
async def gather_posts_api():
    body = await request.json
    list_of_channels = body['channels']
    try:
        await gather_posts(list_of_channels)
        return "start"
    except Exception as e:
        print(e)
        return "couldn't start thread"

