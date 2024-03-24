#!/usr/bin/python3
"""A script that starts a Flask web application.
=> Current file: 6-number_odd_or_even.py"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_route():
    """Returns a simple web page with 'Hello HBNB!'"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb_route():
    """Returns a simple web page with 'HBNB'"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """Returns a simple web page displaying 'C' followed by the value of the
    text variable"""
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_route(text):
    """Returns a simple web page displaying 'Python' followed by value of the
    text variable.
    Default value of text is: 'is cool'"""
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    """Returns a simple web page displaying 'n is a number' only if n is
    an integer"""
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """Returns a simple web page displaying a HTML page only if n is an
    integer:
        H1 tag: “Number: n” inside the tag BODY"""
    return render_template("5-number.html", n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """Returns a simple web page displaying if n is 'odd' or 'even'"""
    return render_template("6-number_odd_or_even.html", n=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
