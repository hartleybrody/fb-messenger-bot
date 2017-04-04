greetings = ["hello", "hi", "get started"]

def process_message(message_payload, message_type):
    responses = []

    if message_payload.lower() in greetings:
        responses.append("Hello there!")
        responses.append(dict(text="In order to better assist you, we'll need your location", get_location=True))

    if message_type == "quick_reply":
        responses.append("You are located at {}".format(message_payload))


    return responses
