#!/usr/bin/env  python3
from flask import Flask, request
from urllib import request as url_request
from bs4 import BeautifulSoup


def get_text(url='http://utopiac.ddns.net:8000'):
    page = url_request.urlopen(url)
    content_page = page.read()
    soup = BeautifulSoup(content_page, "html")
    print(soup.get_text())


app = Flask(__name__)


# prosta aplikacja
@app.route("/")
def hello():
    return "Hello World!!"


# przekazanie parametru z URL
@app.route("/<name>")
def hello_who(name):
    return "Hello " + name + "!!"


# wyspecyfikowanie danych jakich sie oczekuje
@app.route("/age/<int:num>")
def age(num):
    return "You are " + num + " y.o."


# wskazanie by flask uzywal tez metody POST
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # obsłuż dane logowania
        return "zalogowany"
    else:
        # wyświetl formularz logowania
        return "formularz"


if __name__ == "__main__":
#    app.run(host="0.0.0.0", debug=True, port=5000)
    get_text()
