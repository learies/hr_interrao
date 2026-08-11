from collections.abc import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app
from app.settings.config import TestingConfig


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    """Фикстура для создания приложения"""
    app: Flask = create_app(TestingConfig)

    with app.app_context():
        yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Фикстура для создания клиента"""
    return app.test_client()
