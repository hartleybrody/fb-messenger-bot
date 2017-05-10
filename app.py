import os
import sys
import json
import boto3
from pymessenger.bot import Bot

import requests
from flask import Flask, request

app = Flask(__name__)
bot = Bot("EAAD0GgditLsBAEOaCmRSpSHZCcer6BsGNizdj0KPiodpsNWK1a76s9GBDfiUk5uPVWKqOdEM3WnAeJSGQs68tYA4obE56pRCr7GvQr1B7E6W6giAxEIQxZBA7ZA0HVkrtoj3NiOHT1JZCqvDzRcfFVfk87MbVWpowF0H1mEOogZDZD")#Bot(os.environ["PAGE_ACCESS_TOKEN"])

chocolateDict = {
    "snickers",
    "M&M",
    "Twix",
    "Hershey"
}

fruityDict = {
    "jolly rancher",
    "fruit loops",
    "fruity pebbles"
}

candyCategory = {
    "chocolate": chocolateDict,
    "fruity": fruityDict
}

sdb = boto3.client('sdb')

domainName = 'steven.hernandez'

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
                    candyDb = {
                        'Name': 'candy',
                        'Attributes': []
                    }

                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    log(messaging_event["message"])
                    if "text" in messaging_event["message"]:
                        message_text = messaging_event["message"]["text"]  # the message's text

                        if message_text in candyCategory:
                            send_candy_options(sender_id, message_text)
                            return "ok", 200

                        if "payload" in messaging_event["message"]:
                            response = sdb.get_attributes(
                                DomainName = domainName,
                                ItemName = 'candy'
                            )
                            log(response["Attributes"])
                            for candy in response["Attributes"]:
                                log(candy)
                                if candy["Name"].lower() == message_text.lower():
                                    log(candy["Value"])
                                    candy["Value"] =  str(int(candy["Value"]) - 1)
                                    log(candy["Value"])
                                    candy["Replace"] = True
                                    log(candy)

                            log(response["Attributes"])
                            candyDb["Attributes"] = response["Attributes"]
                            sdb.batch_put_attributes(
                                DomainName = domainName,
                                Items = [candyDb]
                            )
                            log("Posting to bother Oren")
                            user_info = get_user_info(sender_id)
                            candy_request = {"senderId": sender_id, "choice": message_text, "name": user_info['first_name'] + " " + user_info['last_name']}
                            r = requests.post("https://iimhlox1ml.execute-api.us-east-1.amazonaws.com/hackathon/candy-request?requestId=gibberish", data=json.dumps(candy_request))
                            #log(r)
                            send_quick_reply(sender_id, {})

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback") or messaging_event.get("referral"):  # user clicked/tapped "postback" button in earlier message
                    log("Referral or postback")
                    log(messaging_event)
                    send_quick_reply(sender_id, {})

    return "ok", 200

@app.route('/solicit-review', methods=['GET'])
def solicit_review():
    sender_id = request.args.get('senderId')
    candy = request.args.get('candy')
    user_info = get_user_info(sender_id)
    request_message = "Hello " + user_info["first_name"] + ",\nHow would you rate your " + candy + "?"
    log("Request message: " + request_message)
    quick_replies = [
        {
            "content_type":"text",
            "title":"1",
            "payload":"1 star",
            "image_url":"https://cdn4.iconfinder.com/data/icons/small-n-flat/24/star-128.png"
        },
        {
            "content_type":"text",
            "title":"2",
            "payload":"2 stars",
            "image_url":"https://cdn4.iconfinder.com/data/icons/small-n-flat/24/star-128.png"
        },
        {
            "content_type":"text",
            "title":"3",
            "payload":"3 stars",
            "image_url":"https://cdn4.iconfinder.com/data/icons/small-n-flat/24/star-128.png"
        },
        {
            "content_type":"text",
            "title":"4",
            "payload":"4 stars",
            "image_url":"https://cdn4.iconfinder.com/data/icons/small-n-flat/24/star-128.png"
        },
        {
            "content_type":"text",
            "title":"5",
            "payload":"5 stars",
            "image_url":"https://cdn4.iconfinder.com/data/icons/small-n-flat/24/star-128.png"
        }
    ]
    bot.send_message(sender_id, {"text": request_message, "quick_replies": quick_replies})
    return "ok", 200

def get_user_info(sender_id):
    url = "https://graph.facebook.com/v2.6/" + sender_id + "?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=EAAD0GgditLsBADZAkcimL0Geyg9r9VyGFvCGoVFm5YhNlZCw3fliqbqXZB5lWnNJnGSm5oMLZCZBZCuRSHqHMgyBimmDl09MVZCcOAmnspRxsGYVTqIsleWogSAeaWvQXDcmr7rqlZAW962UgdgEwTNrDaTTqhQHqhas1I3KcYwRxwZDZD"
    info = requests.get(url)
    log(url)
    log(info.json())
    return info.json()

def send_quick_reply(recipient_id, options):
    info = get_user_info(recipient_id)
    greeting = "Hello "
    if info["gender"] == "male":
        greeting += "Mr. Bond... I mean " + info["last_name"]
    else:
        greeting += "miss " + info["last_name"]

    options = {
        "text": greeting + "\nThank you for picking SCRUBS candy\nPick a candy category you'd like to choose from:",
        "quick_replies":[]
    }
    for key in candyCategory:
        options['quick_replies'].append({
            "content_type":"text",
            "title":key,
            "payload":key,
            "image_url":"https://cdn0.iconfinder.com/data/icons/food-volume-1-4/48/78-512.png"
        })

    log("You should get a message")
    bot.send_message(recipient_id, options)


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": "EAAD0GgditLsBAEOaCmRSpSHZCcer6BsGNizdj0KPiodpsNWK1a76s9GBDfiUk5uPVWKqOdEM3WnAeJSGQs68tYA4obE56pRCr7GvQr1B7E6W6giAxEIQxZBA7ZA0HVkrtoj3NiOHT1JZCqvDzRcfFVfk87MbVWpowF0H1mEOogZDZD"
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

def send_candy_options(recipient_id, category):

    response = sdb.get_attributes(
        DomainName = domainName,
        ItemName = 'candy'
    )
    candyAmount = 0
    candyDict = {}
    for candy in response["Attributes"]:
        candyDict[candy["Name"].lower()] = candy["Value"]

    options = {
        "text": "Choose yo candy",
        "quick_replies":[]
    }

    for key in candyCategory[category]:
        log(candyDict[key.lower()])
        if int(candyDict[key.lower()].lower()) > 0:
            options['quick_replies'].append({
                "content_type":"text",
                "title":key,
                "payload":category,
                "image_url":"https://cdn0.iconfinder.com/data/icons/food-volume-1-4/48/78-512.png"
            })
    log("You should get a message")
    bot.send_message(recipient_id, options)

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
