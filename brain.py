import json

greetings = ["hello", "hi", "get started"]

def process_message(message_payload, message_type):
    responses = []

    if message_payload.lower() in greetings:
        responses.append("Hello there!")
        responses.append(dict(text="In order to find nearby cafes, we'll need your location", get_location=True))

    if message_type == "location":
        coordinates = json.loads(message_payload)["coordinates"]
        lat = coordinates["lat"]
        lon = coordinates["long"]
        responses.append("Here's a link with a map to nearby cafes:")
        responses.append("https://www.google.com/maps/search/cafe/@{},{},15z/data=!3m1!4b1".format(lat, lon))


    return responses
