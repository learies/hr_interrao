from flask import Blueprint

account_bp = Blueprint("account", __name__, url_prefix="/api/v1/")

from .users import api  # noqa

__all__ = ("account_bp",)
