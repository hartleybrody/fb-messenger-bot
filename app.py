import os
import sys
import json
from pymessenger.bot import Bot

import requests
from flask import Flask, request

app = Flask(__name__)
bot = Bot("EAAD0GgditLsBAEOaCmRSpSHZCcer6BsGNizdj0KPiodpsNWK1a76s9GBDfiUk5uPVWKqOdEM3WnAeJSGQs68tYA4obE56pRCr7GvQr1B7E6W6giAxEIQxZBA7ZA0HVkrtoj3NiOHT1JZCqvDzRcfFVfk87MbVWpowF0H1mEOogZDZD")#Bot(os.environ["PAGE_ACCESS_TOKEN"])
#accessKey = os.environ["ACCESS_KEY"]
#secretKey = os.environ["SECRET_KEY"]

candyDict = {
    "jolly rancher":100,
    "snickers":5,
    "M&M":3,
    "Twix":1,
    "Hershey":0
}

#sdb = boto3.client('sdb')

#domainName = 'steven.hernandez'

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
                sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message

                if messaging_event.get("message"):  # someone sent us a message

                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    if message_text in candyDict and candyDict[message_text] > 0:
                        global candyDict
                        candyDict = messaging_event["message"]["payload"]
                        r = requests.post("https://console.aws.amazon.com/apigateway/home?region=us-east-1#/apis/iimhlox1ml/resources/bgfbzu", data=candyDict)

                    #log(bot.get_user_info(sender_id))
                    #bot.send_text_message(sender_id, "roger that!")
                    send_quick_reply(sender_id, {})

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback") or messaging_event.get("referral"):  # user clicked/tapped "postback" button in earlier message
                    send_quick_reply(sender_id, {})

    return "ok", 200

def send_quick_reply(recipient_id, options):

    options = {
        "text":"Thank you for picking SCRUBS candy\nPick a candy:",
        "quick_replies":[]
    }
    for key in candyDict:
        if candyDict[key] > 0:
            options['quick_replies'].append({
                "content_type":"text",
                "title":key,
                "payload":candyDict,
                "image_url":"https://cdn0.iconfinder.com/data/icons/food-volume-1-4/48/78-512.png"
            })

    log(options)
    bot.send_message(recipient_id, options)


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
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
