from typing import Sequence
from uuid import UUID

from app.core.services import BaseService
from app.settings.database import get_db_session

from .dto import WorkerResponseDTO
from .models import WorkerModel
from .repositories import WorkerRepository


class WorkerService(BaseService[WorkerModel, WorkerRepository]):
    """Сервис для работы с сотрудниками."""

    def _get_response_dto(self, worker: WorkerModel) -> WorkerResponseDTO:
        """Получение DTO для сотрудника."""
        return WorkerResponseDTO(
            id=worker.id,
            name=worker.name,
            email=worker.email,
            active=worker.active,
        )

    def get_all(self) -> Sequence[WorkerResponseDTO]:
        """Возвращает всех сотрудников."""
        workers = self.repository.get_all()
        return [self._get_response_dto(worker) for worker in workers]

    def get_by_id(self, id: UUID) -> WorkerResponseDTO | None:
        """Возвращает сотрудника по идентификатору."""
        worker = self.repository.get_by_id(id)
        return self._get_response_dto(worker) if worker is not None else None


def get_worker_service() -> WorkerService:
    """Получение сервиса для работы с сотрудниками."""
    session = get_db_session()
    repository = WorkerRepository(model=WorkerModel, session=session)
    return WorkerService(repository=repository)
