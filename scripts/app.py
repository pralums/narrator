from dis import dis
from operator import truediv
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

# Print all karma objects
def print_db():
    print("Karma DB entries:\n")
    for doc in collection.find({}):
        print(doc)
    print('\n---')

# Add/remove karma from db entries
def karmic_repercussion(item, effect):
    if effect == 'plus':
        db_update({"protagonist": item }, 1)
    else:
        db_update({"protagonist": item }, -1)

def find_karma(item, plus_or_minus, say):
    db_entry = collection.find_one({"protagonist": item })
    if db_entry['karma']:
        if plus_or_minus == "plus":
            print(db_entry)
            # TODO: use this syntax to pull in random karmic phrases:
            # stuff_in_string = "{} something something. ({} karma)".format(item, karma)
            # From https://matthew-brett.github.io/teaching/string_formatting.html
            say(f"\"{item}\" feels warm and fuzzy! ({db_entry['karma']} karma)")
        else:
            print(db_entry)
            say(f"Ouch! \"{item}\" just took a dive! ({db_entry['karma']} karma)")

# For more on this regex, see https://tinyurl.com/5yet7n3z
@app.message(re.compile("(?:\S+)+(?:\s|)(?:\+\+|--)|\(.*?\)(?:\s|)--|\(.*?\)(?:\s|)\+\+"))
def manage_karma(context, say):
    print_db()
    for item in context['matches']:
        plus_or_minus = 'plus' if ('++' in item) else 'minus'
        item = re.sub('--|\+\+','',item) 
        item = re.sub('(?:(?<=\))\s)|(?:\(|\))','',item).strip()
        if '@' in item:
            item = find_display_name(item)
        karmic_repercussion(item,plus_or_minus)
        find_karma(item, plus_or_minus, say)

@app.command("/karma help")
def repeat_text(ack, respond, command):
    ack()
    respond(f"{command['text']}")

@app.command("/karma delete")
def repeat_text(ack, respond, command):
    ack()
    respond(f"{command['text']}")

@app.command("/karma reset")
def repeat_text(ack, respond, command):
    ack()
    respond(f"{command['text']}")    


# Start app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()