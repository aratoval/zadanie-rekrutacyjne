from app import app, db
from app.models import Tasks, Paths
from flask import jsonify, request, make_response


tasks_dict = {}


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """View all tasks
    """
    tasks = Tasks.query.all()
    return jsonify([str(i) for i in tasks]), 200


@app.route("/api/tasks/<int:id>", methods=["GET"])
def get_tasks_of_id(id):
    task = Tasks.query.get(id)
    if task:
        return jsonify(str(task))
    else:
        return "Not found task of id: {}".format(id), 404


@app.route("/api/text/<path:url>", methods=["POST"])
def add_task_text(url):
    t = Tasks(task_type=0, url=url, status='added')
    db.session.add(t)
    db.session.commit()
    return jsonify(str(t)), 201


@app.route("/api/image/<path:url>", methods=["POST"])
def add_task_image(url):
    t = Tasks(task_type=1, url=url, status='added')
    db.session.add(t)
    db.session.commit()
    return jsonify(str(t)), 201


@app.route("/api/downloads/<id>", methods=["GET"])
def downloads(id):
    t = Tasks.query.get(id)
    p = Paths.query.filter_by(task_id=t.id).all()

    return jsonify(str(p))


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
