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
        if message_payload == "hours":
            responses.append("Our store hours are Monday through Friday, from 9am to 6pm.")

        if message_payload == "location":
            responses.append("We are located in the middle of downtown.")


    return responses
