from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def faq():

    # when endpoint is registered as a webhook, it must
    # return the 'hub.challenge' value in the query arguments
    if request.args.get("hub.challenge"):
        return request.args["hub.challenge"]

    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)
