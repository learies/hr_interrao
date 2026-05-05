from http import HTTPStatus
from uuid import UUID

from app.blueprints.parus.pagination import Pagination
from app.blueprints.parus.workers.dto import WorkerResponseDTO
from app.blueprints.parus.workers.query import WorkerQuery

WORKER_ID = UUID("00000000-0000-0000-0000-000000000001")

WORKER_DTO = WorkerResponseDTO(
    id=WORKER_ID,
    name="Иванов Иван",
    email="ivanov@example.com",
    is_active=True,
    is_admin=False,
    last_login=None,
)

WORKER_JSON = {
    "id": str(WORKER_ID),
    "name": "Иванов Иван",
    "email": "ivanov@example.com",
    "is_active": True,
    "is_admin": False,
    "last_login": None,
}


class FakeWorkerService:
    """Фейковый сервис для работы с сотрудниками."""

    def get_all(self, query: WorkerQuery) -> Pagination[WorkerResponseDTO]:
        """Возвращает список сотрудников."""
        return Pagination(
            items=(WORKER_DTO,),
            page=1,
            per_page=20,
            total=1,
        )

    def get_by_id(self, worker_id: UUID) -> WorkerResponseDTO | None:
        """Возвращает сотрудника по идентификатору."""
        assert worker_id == WORKER_ID

        return WORKER_DTO


class FakeWorkerNotFoundService:
    """Фейковый сервис, который не находит сотрудника."""

    def get_by_id(self, worker_id: UUID) -> WorkerResponseDTO | None:
        """Возвращает отсутствие сотрудника."""
        return


def test_get_workers_returns_workers(client, monkeypatch) -> None:
    """Проверяет успешный ответ со списком сотрудников."""
    monkeypatch.setattr(
        "app.blueprints.parus.workers.api.build_worker_service",
        lambda: FakeWorkerService(),
    )

    response = client.get("/api/v1/workers")

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {
        "items": [WORKER_JSON],
        "pagination": {
            "page": 1,
            "per_page": 20,
            "total": 1,
            "pages": 1,
        },
    }


def test_get_worker_returns_worker(client, monkeypatch) -> None:
    """Проверяет успешный ответ с сотрудником по идентификатору."""
    monkeypatch.setattr(
        "app.blueprints.parus.workers.api.build_worker_service",
        lambda: FakeWorkerService(),
    )

    response = client.get(f"/api/v1/worker/{WORKER_ID}")

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == WORKER_JSON


def test_get_worker_returns_404_when_worker_not_found(client, monkeypatch) -> None:
    """Проверяет ответ 404, когда сотрудник не найден."""
    monkeypatch.setattr(
        "app.blueprints.parus.workers.api.build_worker_service",
        lambda: FakeWorkerNotFoundService(),
    )

    response = client.get(f"/api/v1/worker/{WORKER_ID}")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json() == {"error": "Сотрудник не найден"}
