from dis import dis
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from pymongo import MongoClient
from pprint import pprint
import re

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# MongoDB
client = MongoClient()
db = client.karma_db

collection = db.karma_db

#post = {"author": "Mike",
#        "text": "My first blog post!",
#        "tags": ["mongodb", "python", "pymongo"],
#        "date": datetime.datetime.utcnow()
#       }

#posts = db.posts
#post_id = posts.insert_one(post).inserted_id
#print(db.list_collection_names())

#pprint.pprint(posts.find_one())

#print(post_id)

# Listens to incoming messages that contain "hello"
# To learn available listener arguments,
# visit https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
#@app.message("hello")
#def message_hello(message, say):
#    # say() sends a message to the channel where the event was triggered
#    say(f"Hey there <@{message['user']}>!")

def find_display_name(user):
    slack_user = re.sub('>','',re.sub('<','',re.sub('@','',user.strip())))
    profile = app.client.users_profile_get(user=slack_user)
    display_name = profile['profile']['display_name']
    return display_name


@app.message("\+\+")
def add_karma(message, say):
    # print(message)
    temp_array = message['text'].split('++')
    items = []

    for item in temp_array:
        if not item == '':
            if '@' in item:
                display_name = find_display_name(user=item)
                items.append(display_name)
            else: 
                items.append(item.strip())
    for item in items:
        db_stuff

    say(f"I found the following items: {items}")

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()