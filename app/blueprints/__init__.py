from flask import Flask

from .account import account_bp
from .parus import workers_api, workers_views


def register_blueprints(app: Flask) -> None:
    """Регистрация блюпринтов."""
    app.register_blueprint(account_bp)
    app.register_blueprint(workers_api)
    app.register_blueprint(workers_views)
