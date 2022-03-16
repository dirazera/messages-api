import os
os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

import pytest
from messages import app as application
from tests.db_setup import do_db_create, do_db_drop, do_db_seed


@pytest.fixture()
def app():
    application.config.update({
        "TESTING": True,
    })
    yield application


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def db_init_with_data():
    do_db_drop()
    do_db_create()
    do_db_seed()


@pytest.fixture()
def db_init():
   do_db_drop()
   do_db_create()
