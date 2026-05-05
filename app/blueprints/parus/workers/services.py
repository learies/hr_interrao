from collections.abc import Mapping, Sequence
from types import MappingProxyType
from uuid import UUID

from app.blueprints.account.users.dto import UserResponseDTO
from app.blueprints.account.users.services import UserService, build_user_service
from app.settings.database import get_db_session

from ..pagination import Pagination
from ..services import ParusService
from .dto import WorkerResponseDTO
from .models import WorkerModel
from .query import WorkerQuery
from .repositories import WorkerRepository


class WorkerService(ParusService[WorkerModel, WorkerRepository]):
    """Сервис для работы с сотрудниками."""

    def __init__(self, repository: WorkerRepository, user_service: UserService):
        super().__init__(repository)
        self.user_service = user_service

    def get_all(self, query: WorkerQuery) -> Pagination[WorkerResponseDTO]:
        """Возвращает всех сотрудников."""
        users: tuple[UserResponseDTO, ...] | None = None
        worker_ids: tuple[UUID, ...] | None = None

        if query.is_admin is True:
            users = self.user_service.get_admins()
            worker_ids = tuple(user.id for user in (users or ()))

        workers: Sequence[WorkerModel] = self.repository.get_all(
            offset=query.offset,
            limit=query.limit,
            search=query.search,
            is_active=query.is_active,
            worker_ids=worker_ids,
        )
        total: int = self.repository.count_all(
            search=query.search,
            is_active=query.is_active,
            worker_ids=worker_ids,
        )

        return self._build_pagination(
            workers, query.page, query.per_page, total, users=users
        )

    def get_by_id(self, worker_id: UUID) -> WorkerResponseDTO | None:
        """Возвращает сотрудника по идентификатору."""
        worker: WorkerModel | None = self.repository.get_by_id(worker_id)

        return (
            self._build_worker_dtos(workers=[worker])[0] if worker is not None else None
        )

    def _build_users_map(
        self, users: tuple[UserResponseDTO, ...]
    ) -> Mapping[UUID, UserResponseDTO]:
        """Возвращает read-only маппинг пользователей по ID сотрудника."""
        return MappingProxyType({user.id: user for user in (users or ())})

    def _build_worker_dtos(
        self,
        *,
        workers: Sequence[WorkerModel],
        users: tuple[UserResponseDTO, ...] | None = None,
    ) -> tuple[WorkerResponseDTO, ...]:
        """Возвращает DTO сотрудников с обогащёнными данными пользователей."""
        if users is None:
            worker_ids = tuple(worker.id for worker in workers)
            users = self.user_service.get_by_ids(worker_ids)

        users_map = self._build_users_map(users=users)

        return tuple(
            WorkerResponseDTO(
                id=w.id,
                name=w.name,
                email=w.email,
                is_active=w.is_active,
                is_admin=users_map[w.id].is_admin if w.id in users_map else False,
                last_login=users_map[w.id].last_login if w.id in users_map else None,
            )
            for w in workers
        )

    def _build_pagination(
        self,
        workers: Sequence[WorkerModel],
        page: int,
        per_page: int,
        total: int,
        *,
        users: tuple[UserResponseDTO, ...] | None = None,
    ) -> Pagination[WorkerResponseDTO]:
        """Возвращает пагинации."""
        return Pagination(
            items=self._build_worker_dtos(workers=workers, users=users),
            page=page,
            per_page=per_page,
            total=total,
        )


def build_worker_service() -> WorkerService:
    """Получение сервиса для работы с сотрудниками."""
    repository = WorkerRepository(model=WorkerModel, session=get_db_session())
    return WorkerService(repository=repository, user_service=build_user_service())
