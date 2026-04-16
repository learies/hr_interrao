from http import HTTPMethod, HTTPStatus
from uuid import UUID

from flask import jsonify, request
from flask.wrappers import Response

from app.blueprints.parus import parus_bp

from .query import WorkerQuery
from .services import get_worker_service


@parus_bp.route(
    "/workers",
    methods=(HTTPMethod.GET,),
    endpoint="get_workers",
)
def get_workers() -> tuple[Response, HTTPStatus]:
    """Получение списка сотрудников."""
    query = WorkerQuery.from_request(request.args)
    worker_service = get_worker_service()
    workers = worker_service.get_all(query)
    return jsonify(
        {
            "items": [worker.to_dict() for worker in workers.items],
            "pagination": {
                "page": workers.page,
                "per_page": workers.per_page,
                "total": workers.total,
                "pages": workers.pages,
            },
        }
    ), HTTPStatus.OK


@parus_bp.route(
    "/worker/<uuid:worker_id>",
    methods=(HTTPMethod.GET,),
    endpoint="get_worker",
)
def get_worker(worker_id: UUID) -> tuple[Response, HTTPStatus]:
    """Получение сотрудника по идентификатору."""
    worker_service = get_worker_service()
    worker = worker_service.get_by_id(worker_id)
    if worker is not None:
        return jsonify(worker.to_dict()), HTTPStatus.OK
    return jsonify({"error": "Сотрудник не найден"}), HTTPStatus.NOT_FOUND
