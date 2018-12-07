from os import path


basedir = path.abspath(path.dirname(__file__))


class Config(object):

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(
                                                 basedir, "database/task.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
