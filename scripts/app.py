# from dis import dis
# from operator import truediv
from gc import collect
import os
import re
import logging

from typing import Callable
from slack_bolt import App, BoltContext
from slack_bolt.adapter.socket_mode import SocketModeHandler

from pymongo import MongoClient, ReturnDocument
from pprint import pprint

logging.basicConfig(filename='src/logs/narrator.log', encoding='utf-8', level=logging.WARNING)

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
mongo_user = os.environ.get("MONGO_USERNAME")
mongo_password = os.environ.get("MONGO_PASSWORD")

# MongoDB
client = MongoClient(
    username=mongo_user,
    password=mongo_password
)

db = client.karma_db
collection = db.karma_db

# middleware function
def extract_subtype(body: dict, context: BoltContext, next: Callable):
    context["subtype"] = body.get("event", {}).get("subtype", None)
    next()

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

def sort_karma(value, doc, say):
    n = 1
    karma_collection = collection.find().sort('karma', value)
    karma_map = {}
    for x in karma_collection[0:5]:
        karma_map[x['protagonist']]=x["karma"]
    for entry in karma_map:
        doc += f"{n}. {entry}: {karma_map[entry]} karma\n"
        n += 1
    say(doc)

'''
Captures all input followed by `++` or `--`. Allows either a space or no space. 
Phrases must be enclosed in parentheses.

To test this regex, see https://tinyurl.com/5yet7n3z
'''
@app.message(re.compile("(?:\S+)+(?:\s|)(?:\+\+|--)|\(.*?\)(?:\s|)--|\(.*?\)(?:\s|)\+\+"))
def manage_karma(context, say):
    # print_db()
    for item in context['matches']:
        plus_or_minus = 'plus' if ('++' in item) else 'minus'
        item = re.sub('--|\+\+','',item) 
        item = re.sub('(?:(?<=\))\s)|(?:\(|\))','',item).strip()
        if '@' in item:
            item = find_display_name(item)
        karmic_repercussion(item,plus_or_minus)
        find_karma(item, plus_or_minus, say)

'''
Captures `!karma` and a space followed by a single word or a phrase in parentheses.

To test this regex, see https://tinyurl.com/mr24j89j.
'''
@app.message(re.compile("(?<=!karma\s)(?:(?:[^-\(\s]+))|(?<=!karma\s\()(?:[^\)]+)"))
def check_karma(context, say):
    for item in context['matches']:
        db_entry = collection.find_one({"protagonist": item })
        if db_entry:
            say(f"{item} has {db_entry['karma']} karma")
        else:
            say(f"I'm sorry, I didn't find an entry for \"{item}\"")

@app.message(re.compile("!best"))
def best_karma(say):
    sort_karma(-1, "Karmic champions\n", say)

@app.message(re.compile("!worst"))
def worst_karma(say):
    sort_karma(1, "Karmic victims:\n", say)

#@app.message(re.compile("(?<=!delete\s)(?:(?:[^-\(\s]+))|(?<=!delete\s\()(?:[^\)]+)"))
#def delete_entry(context, say):
#    for item in context['matches']:
##        db_entry = collection.find_one({"protagonist": item })
 #       if db_entry:
 #           collection.delete_one({"protagonist": item})
 #           say(f"Deleted {item}")

@app.message(re.compile('!list'))
def list_entries():
    print_db()

@app.command("/karma help")
def repeat_text(ack, respond, command):
    ack()
    respond(f"{command['text']}")

# This listener handles all uncaught message events
# (The position in source code matters)
@app.event({"type": "message"}, middleware=[extract_subtype])
def just_ack(logger, context):
    subtype = context["subtype"]  # by extract_subtype
    logger.info(f"{subtype} is ignored")

# Start app
if __name__ == "__main__":
    SocketModeHandler(
        app,
        os.environ["SLACK_APP_TOKEN"], 
        ping_pong_trace_enabled=True,
        trace_enabled=True
    ).start()