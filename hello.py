#To run, create virtual environment:
#python3 -m venv venv
#. venv/bin/activate
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"