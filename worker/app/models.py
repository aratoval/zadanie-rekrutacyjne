from app import db


class Tasks(db.Model):
    db.__tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    task_type = db.Column(db.Integer)
    url = db.Column(db.Text)
    status = db.Column(db.Integer)
    paths = db.relationship('Paths', lazy='dynamic', backref='files')

    def __repr__(self):
        task_dict = {
            "id": self.id,
            "task_type": self.task_type,
            "url": self.url,
            "status": self.status
        }
        return str(task_dict)


class Paths(db.Model):
    db.__tablename__ = "paths"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=False)
    path = db.Column(db.Text)

    def __repr__(self):
        path_dict = {
            "id": self.id,
            "task_id": self.task_id,
            "path": self.path
        }
        return str(path_dict)
