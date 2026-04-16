from flask import Blueprint

parus_bp = Blueprint("parus", __name__, url_prefix="/api/v1/")

from .workers import api  # noqa

__all__ = ("parus_bp",)
