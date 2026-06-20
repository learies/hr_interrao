from http import HTTPMethod, HTTPStatus
from uuid import UUID

from flask import abort, render_template, request

import app.blueprints.parus.workers.constants as const
from app.blueprints.parus import workers_views as bp

from ..pagination import Pagination
from .dependencies import get_worker_service
from .dto import WorkerResponseDTO
from .query import WorkerQuery


@bp.route(
    const.WORKERS_PATH,
    methods=(HTTPMethod.GET,),
    endpoint=const.WORKERS_ENDPOINT,
)
def get_workers() -> str:
    """Получение списка сотрудников."""
    query = WorkerQuery.from_request(request.args)
    pagination: Pagination[WorkerResponseDTO] = get_worker_service().get_all(query)
    return render_template(const.WORKERS_TEMPLATE, pagination=pagination)


@bp.route(
    const.WORKER_PATH,
    methods=(HTTPMethod.GET,),
    endpoint=const.WORKER_ENDPOINT,
)
def get_worker(worker_id: UUID) -> str:
    """Получение сотрудника по идентификатору."""
    worker: WorkerResponseDTO | None = get_worker_service().get_by_id(worker_id)
    if worker is None:
        abort(HTTPStatus.NOT_FOUND)
    return render_template(const.WORKER_TEMPLATE, worker=worker)
