from typing import Sequence
from uuid import UUID

from app.blueprints.account.users.dto import UserResponseDTO
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
            search_by=query.search_by,
            search=query.search,
            filter_by=query.filter_by,
            filter=query.filter,
        )
        total = self.repository.count_all(
            search_by=query.search_by,
            search=query.search,
            filter_by=query.filter_by,
            filter=query.filter,
        )
        return self._build_paginated_response(workers, query, total)

    def get_by_id(self, worker_id: UUID) -> WorkerResponseDTO | None:
        """Возвращает сотрудника по идентификатору."""
        worker = self.repository.get_by_id(worker_id)
        return self._build_worker_dtos([worker])[0] if worker is not None else None

    def _get_users_by_worker_id(
        self, workers: Sequence[WorkerModel]
    ) -> dict[UUID, UserResponseDTO]:
        """Возвращает пользователей, сгруппированных по идентификатору сотрудника."""
        worker_ids = [worker.id for worker in workers]
        users = self.user_service.get_by_ids(worker_ids)
        return {user.id: user for user in users}

    def _build_worker_dtos(
        self, workers: Sequence[WorkerModel]
    ) -> Sequence[WorkerResponseDTO]:
        """Получение DTO для списка сотрудников."""
        users_by_worker_id = self._get_users_by_worker_id(workers)
        worker_dtos: list[WorkerResponseDTO] = []
        for worker in workers:
            user = users_by_worker_id.get(worker.id)
            worker_dtos.append(
                WorkerResponseDTO(
                    id=worker.id,
                    name=worker.name,
                    email=worker.email,
                    is_active=worker.is_active,
                    is_admin=user.is_admin if user else False,
                    last_login=user.last_login if user else None,
                )
            )
        return worker_dtos

    def _build_paginated_response(
        self, workers: Sequence[WorkerModel], query: WorkerQuery, total: int
    ) -> Pagination[WorkerResponseDTO]:
        """Получение пагинации для списка сотрудников."""
        return Pagination(
            items=self._build_worker_dtos(workers),
            page=query.page,
            per_page=query.per_page,
            total=total,
        )


def build_worker_service() -> WorkerService:
    """Получение сервиса для работы с сотрудниками."""
    repository = WorkerRepository(model=WorkerModel, session=get_db_session())
    return WorkerService(repository=repository, user_service=build_user_service())
