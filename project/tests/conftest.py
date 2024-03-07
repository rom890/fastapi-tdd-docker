import os
import pytest

from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

from app.main import create_application
from app.config import get_settings, Settings


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get('DATABASE_URL'))


@pytest.fixture(scope='module')
def test_app():
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override

    with TestClient(app) as test_client:

        yield test_client

    # teardown


@pytest.fixture(scope='module')
def test_app_with_db():
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    register_tortoise(
        app=app,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:

        yield test_client

    # teardown
