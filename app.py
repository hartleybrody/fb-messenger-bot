import os
import sys
import json

import requests
from flask import Flask, request

from brain import process_message

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message

                    if messaging_event["message"].get("text"):  # they sent a text message
                        message_body = messaging_event["message"].get("text")
                        message_type = "text"

                    if messaging_event["message"].get("quick_reply"):  # they sent a quick reply
                        message_body = messaging_event["message"]["quick_reply"]["payload"]
                        message_type = "quick_reply"

                    if messaging_event["message"].get("attachments"):  # they sent an attachment
                        if messaging_event["message"]["attachments"][0]["type"] == "location":  # they sent a location
                            message_body = json.dumps(messaging_event["message"]["attachments"][0]["payload"])
                            message_type = "location"

                    log("Got a {} message from {}: {}".format(message_type, sender_id, message_body))
                    responses = process_message(message_body, message_type)

                    # convert responses to a list, if not already
                    if type(responses) is not list:
                        responses = [responses]

                    for response in responses:
                        msg = build_message(response)
                        send_message(sender_id, msg)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def build_message(response):
    if type(response) is str or type(response) is unicode:
        return dict(text=response)

    if type(response) == dict and "quick_replies" in response.keys():
        buttons = [dict(content_type="text", title=b["label"], payload=b["value"]) for b in response["quick_replies"]]
        return dict(text=response["text"], quick_replies=buttons)

    if type(response) == dict and "get_location" in response.keys():
        return dict(text=response["text"], quick_replies=[dict(content_type="location")])

    else:
        print response
        raise Exception("Don't know how to send a message like that")


def send_message(recipient_id, message_data):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_data))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": message_data
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
