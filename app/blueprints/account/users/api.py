from http import HTTPMethod, HTTPStatus
from uuid import UUID

from flask import jsonify
from flask.wrappers import Response

from app.blueprints.account import account_bp

from .services import get_user_service


@account_bp.route("/users", methods=(HTTPMethod.GET,))
def get_users() -> tuple[Response, HTTPStatus]:
    """Получение списка пользователей."""
    user_service = get_user_service()
    users = user_service.get_all()
    return jsonify([user.to_dict() for user in users]), HTTPStatus.OK


@account_bp.route("/user/<uuid:user_id>", methods=(HTTPMethod.GET,))
def get_user(user_id: UUID) -> tuple[Response, HTTPStatus]:
    """Получение пользователя по идентификатору."""
    user_service = get_user_service()
    user = user_service.get_by_id(user_id)
    if user is not None:
        return jsonify(user.to_dict()), HTTPStatus.OK
    return jsonify({"error": "Пользователь не найден"}), HTTPStatus.NOT_FOUND
