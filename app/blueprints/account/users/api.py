from http import HTTPMethod, HTTPStatus

from flask import jsonify
from flask.wrappers import Response

from app.blueprints.account import account_bp


@account_bp.route("/users", methods=(HTTPMethod.GET,))
def get_users() -> tuple[Response, HTTPStatus]:
    """Получение списка пользователей."""
    return jsonify({"message": "Hello, World!"}), HTTPStatus.OK
