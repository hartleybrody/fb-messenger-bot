from flask import Flask

app = Flask(__name__)

@app.route('/ping/', methods=['GET', 'POST'])
def faq():
    return "PONG"

if __name__ == '__main__':
    app.run(debug=True)
