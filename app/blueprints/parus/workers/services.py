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
        workers: Sequence[WorkerModel] = self.repository.get_all(
            offset=query.offset,
            limit=query.limit,
            search_by=query.search_by,
            search=query.search,
            filter_by=query.filter_by,
            filter=query.filter,
        )
        total: int = self.repository.count_all(
            search_by=query.search_by,
            search=query.search,
            filter_by=query.filter_by,
            filter=query.filter,
        )

        return self._build_pagination(workers, query.page, query.per_page, total)

    def get_by_id(self, worker_id: UUID) -> WorkerResponseDTO | None:
        """Возвращает сотрудника по идентификатору."""
        worker: WorkerModel | None = self.repository.get_by_id(worker_id)

        return self._build_worker_dtos([worker])[0] if worker is not None else None

    def _map_users_by_worker_ids(
        self, worker_ids: Sequence[UUID]
    ) -> Mapping[UUID, UserResponseDTO]:
        """Возвращает read-only маппинг пользователей по ID сотрудника.

        Пользователи которые отсудствуют в системе, их ID в результат не попадает.
        """
        users: Sequence[UserResponseDTO] = self.user_service.get_by_ids(worker_ids)

        return MappingProxyType({user.id: user for user in (users or ())})

    def _build_worker_dtos(
        self, workers: Sequence[WorkerModel]
    ) -> tuple[WorkerResponseDTO, ...]:
        """Возвращает DTO сотрудников с обагащёнными данными пользователей."""
        worker_ids: tuple[UUID, ...] = tuple(worker.id for worker in workers)
        users_map: Mapping[UUID, UserResponseDTO] = self._map_users_by_worker_ids(
            worker_ids
        )

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
        self, workers: Sequence[WorkerModel], page: int, per_page: int, total: int
    ) -> Pagination[WorkerResponseDTO]:
        """Возвращает пагинации."""
        return Pagination(
            items=self._build_worker_dtos(workers),
            page=page,
            per_page=per_page,
            total=total,
        )


def build_worker_service() -> WorkerService:
    """Получение сервиса для работы с сотрудниками."""
    repository = WorkerRepository(model=WorkerModel, session=get_db_session())
    return WorkerService(repository=repository, user_service=build_user_service())
