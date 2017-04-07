import json

from cache import redis

greetings = ["hello", "hi", "get started"]

def process_message(message_payload, message_type, sender_id):

    convo = get_convo(sender_id)  # load any existing conversation state for this user
    responses = []

    if message_payload.lower() in greetings:
        responses.append("Hello there!")
        responses.append(dict(
            text="What sort of coffehouse are you looking for?",
            quick_replies=[
                dict(label="Dunkin Donuts", value="dunkin donuts"),
                dict(label="Starbucks", value="starbucks"),
                dict(label="Local Cafe", value="cafe"),
            ]))

    if message_type == "quick_reply":
        convo["coffeehouse"] = message_payload  # store the payload of what they sent us in the conversation in redis

        responses.append("Roger that.")
        responses.append(dict(text="In order to find something nearby, we'll need your location.", get_location=True))


    if message_type == "location":
        coordinates = json.loads(message_payload)["coordinates"]
        lat = coordinates["lat"]
        lon = coordinates["long"]

        coffeehouse = convo["coffeehouse"]  # load their coffeehouse preference from this user's conversation state

        responses.append("Here's what I found:")
        responses.append("https://www.google.com/maps/search/{}/@{},{},15z/data=!3m1!4b1".format(coffeehouse, lat, lon))


    set_convo(sender_id, convo)  # make sure we store any changes to the converastion's state back into redis
    return responses

def get_convo(sender_id):
    json_convo = redis.get(sender_id)
    if json_convo:
        return json.loads(json_convo)
    else:  # no existing convo found
        return {}

def set_convo(sender_id, convo):
    if convo:
        redis.set(sender_id, json.dumps(convo))