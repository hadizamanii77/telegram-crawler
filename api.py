import asyncio
import json

from flask import Flask
from flask import request
from tasks import gather_posts

app = Flask(__name__)


@app.route('/api/gather/posts', methods=['POST'])
def gather_posts_api():
    body = json.loads(request.data)
    list_of_channels = body['channels']
    task_id = gather_posts.delay(list_of_channels=list_of_channels)
    return str(task_id)
