from typing import Sequence
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
        active: bool | None,
        search: str | None,
        search_by: str | None,
    ) -> Sequence[WorkerModel]:
        """Возвращает всех сотрудников."""
        stmt = select(self.model)
        stmt = self._apply_active(stmt, active)
        stmt = self._apply_search_filter(stmt, search, search_by)
        return self.session.scalars(stmt.offset(offset).limit(limit)).all()

    def get_by_id(self, worker_id: UUID) -> WorkerModel | None:
        """Возвращает сотрудника по идентификатору."""
        return self.get_by_attribute("id", worker_id)

    def count_all(
        self, active: bool | None, search: str | None, search_by: str | None
    ) -> int:
        """Возвращает количество всех сотрудников."""
        stmt = select(func.count()).select_from(self.model)
        stmt = self._apply_active(stmt, active)
        stmt = self._apply_search_filter(stmt, search, search_by)
        return self.session.scalar(stmt) or 0

    def _apply_active(self, stmt: Select, active: bool | None) -> Select:
        """Применяет фильтр по активности."""
        if active is not None:
            return stmt.where(self.model.active.is_(active))
        return stmt

    def _apply_search_filter(
        self, stmt: Select, search: str | None, search_by: str | None
    ) -> Select:
        """Применяет фильтр по поисковому запросу."""
        if not search:
            return stmt

        if search_by:
            return stmt.where(getattr(self.model, search_by).ilike(f"%{search}%"))

        return stmt.where(
            or_(
                self.model.name.ilike(f"%{search}%"),
                self.model.email.ilike(f"%{search}%"),
            )
        )
