from flask import Flask

from .account import account_bp
from .parus import parus_bp


def register_blueprints(app: Flask) -> None:
    """Регистрация блюпринтов."""
    app.register_blueprint(account_bp)
    app.register_blueprint(parus_bp)
