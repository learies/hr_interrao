from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.sql.selectable import Select

from ..repositories import ParusRepository
from .models import WorkerModel


class WorkerRepository(ParusRepository[WorkerModel]):
    """Репозиторий для работы с сотрудниками."""

    def get_all(
        self,
        offset: int,
        limit: int,
        search: str | None,
        is_active: bool | None,
        worker_ids: Sequence[UUID] | None = None,
    ) -> Sequence[WorkerModel]:
        """Возвращает всех сотрудников."""
        stmt = select(self.model)
        stmt = self._apply_filter_worker_ids(stmt, worker_ids=worker_ids)
        stmt = self._apply_search(stmt, search=search)
        stmt = self._apply_filter_active(stmt, is_active=is_active)
        return self.session.scalars(
            stmt.order_by(self.model.name).offset(offset).limit(limit)
        ).all()

    def get_by_id(self, worker_id: UUID) -> WorkerModel | None:
        """Возвращает сотрудника по идентификатору."""
        return self.get_by_attribute("id", worker_id)

    def count_all(
        self,
        search: str | None,
        is_active: bool | None,
        worker_ids: Sequence[UUID] | None = None,
    ) -> int:
        """Возвращает количество всех сотрудников."""
        stmt = select(func.count()).select_from(self.model)
        stmt = self._apply_filter_worker_ids(stmt, worker_ids=worker_ids)
        stmt = self._apply_search(stmt, search=search)
        stmt = self._apply_filter_active(stmt, is_active=is_active)
        return self.session.scalar(stmt) or 0

    def _apply_filter_worker_ids(self, stmt: Select, worker_ids: Sequence[UUID] | None) -> Select:
        """Применяет фильтрацию по идентификаторам сотрудников."""
        if worker_ids is None or not worker_ids:
            return stmt
        return stmt.where(self.model.id.in_(worker_ids))

    def _apply_filter_active(self, stmt: Select, is_active: bool | None) -> Select:
        """Применяет фильтрацию по активности."""
        if is_active is None:
            return stmt.where(self.model.active.is_(True))
        return stmt.where(self.model.active.is_(is_active))

    def _apply_search(self, stmt: Select, search: str | None) -> Select:
        """Применяет поиск."""
        if not search:
            return stmt

        return stmt.where(
            or_(
                self.model.name.ilike(f"%{search}%"),
                self.model.email.ilike(f"%{search}%"),
            )
        )
