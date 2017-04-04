greetings = ["hello", "hi", "get started"]

def process_message(message_payload, message_type):
    responses = []

    if message_payload.lower() in greetings:
        responses.append("Hello there!")
        responses.append(dict(
                text="What can I help you with today?",
                quick_replies=[
                    dict(label="Store Hours", value="hours"),
                    dict(label="Location", value="location"),
                ]
            ))

    if message_type == "quick_reply":
        responses.append("You clicked a Quick Reply button")

    return responses
