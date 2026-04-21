from typing import Sequence
from uuid import UUID

from app.blueprints.account.users.services import UserService, build_user_service
from app.core.services import BaseService
from app.settings.database import get_db_session

from ..pagination import Pagination
from .dto import WorkerResponseDTO
from .models import WorkerModel
from .query import WorkerQuery
from .repositories import WorkerRepository


class WorkerService(BaseService[WorkerModel, WorkerRepository]):
    """Сервис для работы с сотрудниками."""

    def __init__(self, repository: WorkerRepository, user_service: UserService):
        super().__init__(repository)
        self.user_service = user_service

    def get_all(self, query: WorkerQuery) -> Pagination[WorkerResponseDTO]:
        """Возвращает всех сотрудников."""
        workers = self.repository.get_all(
            offset=query.offset,
            limit=query.limit,
            active=query.active,
            search=query.search,
            search_by=query.search_by,
        )
        total = self.repository.count_all(
            active=query.active,
            search=query.search,
            search_by=query.search_by,
        )
        return self._build_pagination(workers, query, total)

    def get_by_id(self, worker_id: UUID) -> WorkerResponseDTO | None:
        """Возвращает сотрудника по идентификатору."""
        worker = self.repository.get_by_id(worker_id)
        return self._build_response_dtos([worker])[0] if worker is not None else None

    def _attach_user_to_worker(self, workers: Sequence[WorkerModel]) -> None:
        """Прикрепление пользователя к сотруднику."""
        user_ids = [worker.id for worker in workers]
        users = self.user_service.get_by_ids(user_ids)
        users_map = {user.id: user for user in users}
        for worker in workers:
            user = users_map.get(worker.id)
            setattr(worker, "is_admin", user.is_admin if user else False)
            setattr(worker, "last_login", user.last_login if user else None)

    def _build_response_dtos(
        self, workers: Sequence[WorkerModel]
    ) -> Sequence[WorkerResponseDTO]:
        """Получение DTO для списка сотрудников."""
        self._attach_user_to_worker(workers)
        return [
            WorkerResponseDTO(
                id=worker.id,
                name=worker.name,
                email=worker.email,
                is_active=worker.is_active,
                is_admin=getattr(worker, "is_admin", False),
                last_login=getattr(worker, "last_login", None),
            )
            for worker in workers
        ]

    def _build_pagination(
        self, workers: Sequence[WorkerModel], query: WorkerQuery, total: int
    ) -> Pagination[WorkerResponseDTO]:
        """Получение пагинации для списка сотрудников."""
        return Pagination(
            items=self._build_response_dtos(workers),
            page=query.page,
            per_page=query.per_page,
            total=total,
        )


def build_worker_service() -> WorkerService:
    """Получение сервиса для работы с сотрудниками."""
    repository = WorkerRepository(model=WorkerModel, session=get_db_session())
    return WorkerService(repository=repository, user_service=build_user_service())
