import os

from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def webook():

    if not request.args.get("verify_token") == os.environ["VERIFY_TOKEN"]:
        return "Verification token mismatch", 403

    # when endpoint is registered as a webhook, it must
    # return the 'hub.challenge' value in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        return request.args["hub.challenge"]

    print request.form

    return "ok"


if __name__ == '__main__':
    app.run(debug=True)
