#!/usr/bin/env  python3
from flask import Flask, jsonify, request, make_response
import threading
from content_getter import ContentGetter


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
