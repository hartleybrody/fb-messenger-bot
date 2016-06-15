import os
import sys
import json

import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def webook():

    # when endpoint is registered as a webhook, it must
    # return the 'hub.challenge' value in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"]

    data = request.get_json()
    log(data)

    if data["object"] == "page":

        for entry in data["entry"]:
            for message in entry["messaging"]:

                # the facebook ID of the person sending you the message
                sender_id = message["sender"]["id"]

                # the recipient's ID, which should be your page's facebook ID
                recipient_id = message["recipient"]["id"]

                # the timestamp of the message
                timestamp = message["timestamp"]

                # the message ID
                message_id = message["message"]["mid"]

                # the message sequence number
                message_seq = message["message"]["seq"]

                # the message text
                message_text = message["message"]["text"]

                send_message(recipient_id, "got it, thanks!")

    return "ok"


def send_message(recipient_id, message_text):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

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
        "message": {
            "text": message_text
        }
    })
    requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)


def log(message):
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
