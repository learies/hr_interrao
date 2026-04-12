from flask import Flask


def create_app() -> Flask:
    """Создание приложения"""
    app = Flask(__name__)

    return app
