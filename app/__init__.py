from flask import Flask

from app.settings.config import Config, load_config


def create_app(config_class: type[Config]) -> Flask:
    """Создание приложения"""
    app = Flask(__name__)
    app.config.from_object(load_config(config_class))

    return app
