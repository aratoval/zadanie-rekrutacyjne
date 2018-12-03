#!/usr/bin/env  python3
from flask import Flask
from urllib import request as url_request
from bs4 import BeautifulSoup
from asyncio import async


class ContentGetter:

    current_status = ''
    work_type = 0  # 0 - unknown, 1 - get text, 2 - get image, 3 - get all
    workers_list = []

    def __init__(self, url, work_type):
        ContentGetter.workers_list.append(url)
        self.id = url
        self.url = url
        self.status = "running"
        self.work_type = work_type

    def change_status(self):
        self.current_status = 'finished'

    def get_text(self):
        page = url_request.urlopen(self.url)
        content_page = page.read()
        soup = BeautifulSoup(content_page, "html.parser")
        print(soup.get_text())
        return 0

    def get_image(self):
        page = url_request.urlopen(self.url)
        content_page = page.read()
        soup = BeautifulSoup(content_page, "html.parser")
        image_list = soup.find_all('img')
        print(image_list)
        return 0

    def work(self):
        if self.work_type != 0:
            if self.work_type == 1:
                result = self.get_text()
                if result == 0:
                    self.change_status()
            elif self.work_type == 2:
                result = self.get_image()
                if result == 0:
                    self.change_status()
            else:
                result_1 = self.get_text()
                result_2 = self.get_image()
                if result_1 + result_2 == 0:
                    self.change_status()

    def status(self):
        print(self.current_status)


app = Flask(__name__)


tasks_list = []


@app.route("/api/tasks", methods=["GET"])
def tasks():
    return str(ContentGetter.workers_list)


@app.route("/api/tasks/<task_type>/<url>", methods=["POST"])
def run_tasks(task_type, url):
    tasks_list.append(str(url))
    tasks_list[-1] = ContentGetter(url, task_type)
    return str(task_type) + url


# # prosta aplikacja
# @app.route("/", methods=['GET'])
# def hello():
#     return "Hello World!!"
#
#
# # przekazanie parametru z URL
# @app.route("/API/<name>")
# def hello_who(name):
#     return "Hello " + name + "!!"
#
#
# # wyspecyfikowanie danych jakich sie oczekuje
# @app.route("/age/<int:num>")
# def age(num):
#     return "You are " + num + " y.o."
#
#
# # wskazanie by flask uzywal tez metody POST
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # obsłuż dane logowania
#         return "zalogowany"
#     else:
#         # wyświetl formularz logowania
#         return "formularz"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
#    get_text()
#    get_image()
