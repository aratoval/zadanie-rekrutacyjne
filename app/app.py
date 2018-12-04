#!/usr/bin/env  python3
from os import curdir
from flask import Flask, jsonify, request, make_response
from urllib import request as url_request
from bs4 import BeautifulSoup
import threading
import queue


class ContentGetter:

    work_type_dict = {0: "unknown", 1: "get text", 2: "get image", 3: "get all"}
    current_status = ""
    workers_list = []

    def __init__(self, work_type, url):
        ContentGetter.workers_list.append(id(self))
        self.id = id(self)
        self.work_type = work_type
        self.url = url
        self.current_status = 'running'
        # self.work()

    def serialize(self):
        return {
            "id": self.id,
            "work_type": self.work_type,
            "work_type_name": self.work_type_dict[int(self.work_type)],
            "url": self.url,
            "status": self.current_status
        }

    def get_text(self):
        try:
            page = url_request.urlopen(self.url)
            content_page = page.read()
            soup = BeautifulSoup(content_page, "html.parser")
            self.current_status = "finished"
            return soup
        except Exception as e:
            self.current_status = "error: {}".format(e)

    def get_image(self):
        try:
            page = url_request.urlopen(self.url)
            content_page = page.read()
            soup = BeautifulSoup(content_page, "html.parser")
            image_list = soup.find_all('img')
            self.current_status = "finished"
            return image_list
        except Exception as e:
            self.current_status = "error: {}".format(e)

    def status(self):
        return {"status": self.current_status}

    def work(self):
        if self.work_type == 1:
            self.get_text()
        elif self.work_type == 2:
            self.get_image()
        else:
            raise Exception("Incorrect work type")


app = Flask(__name__)


tasks_dict = {}


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify([tasks_dict[id].serialize() for id in tasks_dict.keys()])


@app.route("/api/tasks/<int:id>", methods=["GET"])
def get_tasks_of_id(id):
    return jsonify(tasks_dict[int(id)].status())


@app.route("/api/tasks/text", methods=["POST"])
def create_task_text():
    url = request.args.get("url")
    a = ContentGetter(1, url)
    t = threading.Thread(target=a.work())
    t.setDaemon(True)
    t.start()
    tasks_dict[id(a)] = a
    return jsonify(a.serialize())


@app.route("/api/tasks/image", methods=["POST"])
def create_task_image():
    url = request.args.get("url")
    a = ContentGetter(2, url)
    t = threading.Thread(target=a.work())
    t.setDaemon(True)
    t.start()
    tasks_dict[id(a)] = a
    return jsonify(a.serialize())


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
