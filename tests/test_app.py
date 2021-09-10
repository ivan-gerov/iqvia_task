"""
I attempted to setup the SQLAlchemy database fixture, 
but I couldn't, so I decided to utilize the time needed
to check this at working on the celery task and refactoring
the app.
"""


import tempfile
import pytest 

import os

from app import config
from flask_sqlalchemy import SQLAlchemy
from app.main import create_app, app_blueprint


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    test_app, db = create_app(app_blueprint)
    test_app.config.from_object(config.TestingConfig)
    test_app.config["TESTING"] = True
    test_app.config["SQLACLHEMY_DATABASE_URI"] = f"sqlite:////{db_path}"
    with test_app.test_client() as client:
        yield client
    os.close(db_fd)
    os.unlink(db_path)


def test_list_contacts(client):
    """Test list contacts route"""
    response = client.get("/api/v1/contact")
    raise Exception(response.data)