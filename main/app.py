import os
import re
import logging
import pathlib

# from typing import Callable
from slack_bolt import App, BoltContext
from slack_bolt.adapter.socket_mode import SocketModeHandler

from pymongo import MongoClient, ReturnDocument
from pprint import pprint

mongo_user = os.environ.get("MONGO_USERNAME")
mongo_password = os.environ.get("MONGO_PASSWORD")

dev_environment=os.environ.get("DEV_ENVIRONMENT")
FORMAT = '%(asctime)s %(message)s'

script_location = str(pathlib.Path(__file__).parent.parent.resolve())
log_location = script_location + 'narrator.log'

if dev_environment:
    print(f"DEV ENVIRONMENT: {dev_environment}")
    logging.basicConfig(
        level=logging.WARNING,
        format=FORMAT
    )
    client = MongoClient()

else:
    print(f"DEV ENVIRONMENT: {dev_environment}")
    logging.basicConfig(
        level=logging.WARNING,
        format=FORMAT,
        filename='{}narrator.log',
        encoding='utf-8'
    )
    client = MongoClient(
        username=mongo_user,
        password=mongo_password
    )

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
db = client.tob
collection = db.tob

# middleware function
#def extract_subtype(body: dict, context: BoltContext, next: Callable):
#    context["subtype"] = body.get("event", {}).get("subtype", None)
#    next()

@app.command("/echo")
def repeat_text(ack, respond, command):
    # Acknowledge command request
    ack()
    respond(f"{command['text']}")

# Start bot
if __name__ == "__main__":
    SocketModeHandler(
        app,
        os.environ["SLACK_APP_TOKEN"], 
        ping_pong_trace_enabled=True,
        trace_enabled=True,
        auto_reconnect_enabled=True
    ).start()