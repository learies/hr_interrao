from http import HTTPMethod, HTTPStatus
from uuid import UUID

from flask import jsonify, request
from flask.wrappers import Response

import app.blueprints.parus.workers.constants as const
from app.blueprints.parus import workers_api as bp

from .query import WorkerQuery
from .services import build_worker_service


@bp.route(
    const.WORKERS_PATH,
    methods=(HTTPMethod.GET,),
    endpoint=const.WORKERS_ENDPOINT,
)
def get_workers() -> tuple[Response, HTTPStatus]:
    """Получение списка сотрудников."""
    query = WorkerQuery.from_request(request.args)
    workers = build_worker_service().get_all(query)
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


@bp.route(
    const.WORKER_PATH,
    methods=(HTTPMethod.GET,),
    endpoint=const.WORKER_ENDPOINT,
)
def get_worker(worker_id: UUID) -> tuple[Response, HTTPStatus]:
    """Получение сотрудника по идентификатору."""
    worker = build_worker_service().get_by_id(worker_id)
    if worker is not None:
        return jsonify(worker.to_dict()), HTTPStatus.OK
    return jsonify({"error": "Сотрудник не найден"}), HTTPStatus.NOT_FOUND
