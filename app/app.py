#!/usr/bin/env  python3
from os import curdir, path, mkdir
from flask import Flask, jsonify, request, make_response
from urllib3 import PoolManager
from bs4 import BeautifulSoup
import threading


class ContentGetter:

    work_type_dict = {0: "unknown", 1: "get text", 2: "get image", 3: "get all"}
    current_status = ""
    path_to_data = ""
    workers_list = []
    root_dir_path = ""

    def __init__(self, work_type, url):
        ContentGetter.workers_list.append(id(self))
        self.id = id(self)
        self.work_type = work_type
        self.url = url
        self.current_status = 'running'
        self.root_dir_path = curdir

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
            destiny = "text/{}.txt".format(self.id)
            with open(path.join(self.root_dir_path, destiny), "w") as f:
                page = PoolManager().request("GET", self.url)
                content_page = page.data
                soup = BeautifulSoup(content_page, "html.parser").get_text()
                f.writelines(soup)
                self.current_status = "finished"
            return
        except Exception as e:
            self.current_status = "error: {}".format(e)

    def get_image(self):
        try:
            destiny = "image/{}".format(self.id)
            if not path.exists(destiny):
                mkdir(destiny)

            page = PoolManager()\
                .request("GET", self.url)
            content_page = page.data
            soup = BeautifulSoup(content_page, "html.parser")
            images_list = soup.find_all('img')
            for image in images_list:
                with open(path.join(destiny,
                                    image['src'].split("/")[-1]),
                          "wb") as out_image:
                    http = PoolManager().request(
                            "GET",
                            self.url + image['src'],
                            preload_content = False)
                    while True:
                        data = http.read(1024)
                        if not data:
                            break
                        out_image.write(data)
            self.current_status = "finished"
            return
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


def create_app():
    app = Flask(__name__)

    tasks_dict = {}

    @app.route("/api/tasks", methods=["GET"])
    def get_tasks():
        return jsonify(
                [tasks_dict[id].serialize() for id in tasks_dict.keys()]), 200

    @app.route("/api/tasks/<int:id>", methods=["GET"])
    def get_tasks_of_id(id):
        if id not in tasks_dict.keys():
            return "Not found", 404
        else:
            return jsonify(tasks_dict[int(id)].status()), 200

    @app.route("/api/tasks/text/<url>", methods=["POST"])
    def create_task_text(url):
        a = ContentGetter(1, "http://" + url)
        t = threading.Thread(target=a.work())
        t.setDaemon(True)
        t.start()
        tasks_dict[id(a)] = a
        return jsonify(a.serialize()), 201

    @app.route("/api/tasks/image", methods=["POST"])
    def create_task_image():
        url = request.args.get("url")
        a = ContentGetter(2, url)
        t = threading.Thread(target=a.work())
        t.setDaemon(True)
        t.start()
        tasks_dict[id(a)] = a
        return jsonify(a.serialize()), 201

    @app.route("/api/tasks/downloads/<id>", methods=["GET"])
    def downloads(id):

        return

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", debug=True, port=5000)
