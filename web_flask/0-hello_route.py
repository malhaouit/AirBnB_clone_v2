#!/usr/bin/python3
"""A script that starts a Flask web application and its route ('/'):
    display “Hello HBNB!”
=> Current file: 0-hello_route.py"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_route():
    """Returns a simple web page with 'Hello HBNB!'"""
    return 'Hello HBNB!'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
