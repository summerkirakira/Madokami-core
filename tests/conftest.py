from madokami.db import init_db
import pytest


@pytest.fixture()
def database():
    init_db()
