from flask import Blueprint

workers_api = Blueprint("workers_api", __name__, url_prefix="/api/v1/")
workers_views = Blueprint("workers_views", __name__)

from .workers import api  # noqa
from .workers import views  # noqa

__all__ = (
    "workers_api",
    "workers_views",
)
