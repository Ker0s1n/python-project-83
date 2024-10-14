from flask import (Flask,)


app = Flask(__name__)
app.secret_key = "secret_key"


@app.route('/')
def hello_world():
    return '<h1>Welcome!</h1>'
