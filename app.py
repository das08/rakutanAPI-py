from flask import Flask
from api import api

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

app.register_blueprint(api.app)


@app.route('/')
def root():
    return "Welcome to Rakutan API"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
