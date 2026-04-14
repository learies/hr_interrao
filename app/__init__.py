from typing import Mapping

from flask import Flask

from app.settings.config import Config, load_config
from app.settings.database import db
from app.settings.env import init_env


def create_app(
    config_class: type[Config], *, env: Mapping[str, str] | None = None
) -> Flask:
    """Создание приложения"""
    # Инициализация переменных окружения
    if env is not None:
        init_env()

    # Создание приложения
    app = Flask(__name__)

    # Загрузка конфигурации
    app.config.from_object(load_config(config_class))

    # Инициализация базы данных
    db.init_app(app)

    return app
