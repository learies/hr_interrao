from flask import Flask

from .account import account_bp


def register_blueprints(app: Flask) -> None:
    """Регистрация блюпринтов."""
    app.register_blueprint(account_bp)
