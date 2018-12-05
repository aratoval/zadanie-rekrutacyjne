from os import unlink
import pytest
from flask import url_for


class TestApp:

    def test_tasks_show(self, client):
        res = client.get(url_for("get_tasks"))
        assert res.status_code == 200
        res = client.get(url_for("get_tasks_of_id", id=10))
        assert res.status_code == 404

    def test_tasks_text_add(self, client):
        url = "utopiac.ddns.net:8000"
        res = client\
            .get(url_for("create_task_text", url=url))
        assert res.status_code == 405

        res = client \
            .post(url_for("create_task_text", url = url))
        assert res.status_code == 201
