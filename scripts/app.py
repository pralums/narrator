from dis import dis
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from pymongo import MongoClient, ReturnDocument
from pprint import pprint
import re

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# MongoDB
client = MongoClient()
db = client.karma_db
collection = db.karma_db

# Finds the display_name associated with a Slack user ID
def find_display_name(user):
    slack_user = re.sub('>','',re.sub('<','',re.sub('@','',user.strip())))
    profile = app.client.users_profile_get(user=slack_user)
    display_name = profile['profile']['display_name']
    return display_name

# Handle database updates
def db_update(filter, i):
    if collection.find_one(filter):
        collection.find_one_and_update(
            filter, 
            {'$inc': {'karma': i}},
            return_document=ReturnDocument.AFTER
            )
    else:
        filter['karma'] = i
        collection.insert_one(filter)

# Add/remove karma from db entries
def karmic_repercussion(item, effect):
    if effect == 'plus':
        db_update({"protagonist": item }, 1)
    else:
        db_update({"protagonist": item }, -1)

def find_karma(item):
    db_entry = collection.find_one({"protagonist": item })

@app.message(re.compile("(?:\S+)+(?:\s|)(?:\+\+|--)"))
def manage_karma(context, say):
    #for doc in collection.find({}):
    #    print(doc)
    for item in context['matches']:
        if '++' in item:
            if '@' in item:
                item = find_display_name(re.sub('--','',re.sub('\+\+','', item)))
            item = re.sub('\+\+','',item).strip()
            karmic_repercussion(item,'plus')
            find_karma(item)
        else:
            if '@' in item:
                item = find_display_name(re.sub('--','',re.sub('\+\+','', item)))
            item = re.sub('--','',item).strip()    
            karmic_repercussion(item,'minus')
            find_karma(item)
            #say(f'{karma_item} has lost karma')


# Start app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()