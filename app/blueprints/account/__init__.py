from flask import Blueprint

account_bp = Blueprint("account", __name__, url_prefix="/api/v1/account")

__all__ = ("account_bp",)
