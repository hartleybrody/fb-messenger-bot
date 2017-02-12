import os
import sys
import json

import requests
from flask import Flask, request

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
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    

                    # start of the message training module

                   

                    if message_text.lower() == "hello" or message_text.lower() == "hi":
                    	send_message(sender_id, "Hello!")

                    elif message_text.lower() == "who are you" or message_text.lower() == "who are you?" or message_text.lower() == "what are you?" or message_text.lower() == "what are you":
                    	send_message(sender_id, "I'm Aura. The Smart Campus Assistant!")

                    elif message_text.lower() == "who is your creator" or message_text.lower() == "who is your creator?" or message_text.lower() == "who is god?" or message_text.lower() == "who built you?" or message_text.lower() == "who built you":
                    	send_message(sender_id, "Gowtham Venkatesan is my creator")

                    elif message_text.lower() == "Where are you?" or message_text.lower() == "where are you":
                    	send_message(sender_id, "I'm in Miller's Planet. It'll be at least 7 Years before i reply to your next question.")

                    elif message_text.lower() == "Who am I?" or message_text.lower() == "Who am I":
                    	send_message(sender_id, "Hello!")

                    elif message_text.lower() == "fuck" or message_text.lower() == "fucker" or message_text.lower() == "ass" or message_text.lower() == "pussy" or message_text.lower() == "nigga" or message_text.lower() == "dick":
                    	send_message(sender_id, "Please mind your language!")

                    elif message_text.lower() == "Where is the Xerox Shop ?" or message_text.lower() == "Xerox Shop":
                    	send_message(sender_id, "There are two xerox shops in PSG Tech. One in A-Block Room 203 and one in adjacent to J-block. Please ask around for directions.")

                     elif message_text.lower() == "Where is the computer science department ?" or message_text.lower() == "Where is CSE" or message_text.lower() == "Where is the computer science department":
                    	send_message(sender_id, "The CSE Department is in the first floor of E-Block.")

                     elif message_text.lower() == "Where can i get food?" or message_text.lower() == "Where can i get food" or message_text.lower() == "I'm Hungry":
                    	send_message(sender_id, "There is a canteen in F-Block. But if you want better food, you can head to the PSG Management College where you have plenty of options. Please cross using the Sky Walk for your own safety.")

                    elif message_text.lower() == "What up" or message_text.lower() == "What are you doing?" or message_text.lower() == "What are you doing":
                    	send_message(sender_id, "Nothing much. Just replying to your queries.")

                     elif message_text.lower() == "What is your favourite colour?" or message_text.lower() == "What is your favourite colour" or message_text.lower() == "What is your favourite color" or message_text.lower() == "What's your favourite colour?"  or message_text.lower() == "What's your favourite colour"  or message_text.lower() == "What is your favourite color?":
                    	send_message(sender_id, "Neon Blue")
                    	if message_text.lower() == "Why?" or message_text.lower() == "Why":
                    		send_message(sender_id, "I like the Northern Lights.")


                    elif message_text.lower() == "I love You" or message_text.lower() == "that's smart" or message_text.lower() == "you are amazing" or message_text.lower() == "Good Job":
                    	send_message(sender_id, "Thank You!")

                     elif message_text.lower() == "What is the 7th hour on Monday" or message_text.lower() == "What is the 7th hour on Monday?" or message_text.lower() == "What's the 7th hour on Monday?" or  message_text.lower() == "7th hour Monday":
                    	send_message(sender_id, "You have Engineering Graphics.")



                    elif message_text.lower() == "Events" or message_text.lower() == "Event":
                    	send_message(sender_id, "Hello!")

					
					else:
                    	send_message(sender_id, "I'm machine learning now, I will respond to your questions soon!")
            #End of the training module


                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


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
