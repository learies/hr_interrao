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
        search_by: str | None,
        search: str | None,
        filter_by: str | None,
        filter: bool | None,
    ) -> Sequence[WorkerModel]:
        """Возвращает всех сотрудников."""
        stmt = select(self.model)
        stmt = self._apply_search(stmt, search_by=search_by, search=search)
        stmt = self._apply_filter(stmt, filter_by=filter_by, filter=filter)
        return self.session.scalars(stmt.offset(offset).limit(limit)).all()

    def get_by_id(self, worker_id: UUID) -> WorkerModel | None:
        """Возвращает сотрудника по идентификатору."""
        return self.get_by_attribute("id", worker_id)

    def count_all(
        self,
        search_by: str | None,
        search: str | None,
        filter_by: str | None,
        filter: bool | None,
    ) -> int:
        """Возвращает количество всех сотрудников."""
        stmt = select(func.count()).select_from(self.model)
        stmt = self._apply_search(stmt, search_by=search_by, search=search)
        stmt = self._apply_filter(stmt, filter_by=filter_by, filter=filter)
        return self.session.scalar(stmt) or 0

    def _apply_filter(
        self,
        stmt: Select,
        filter_by: str | None,
        filter: bool | None,
    ) -> Select:
        """Применяет фильтрацию."""
        if filter is None:
            return stmt
        if filter_by:
            if filter_by == "is_active":
                return stmt.where(self.model.active.is_(filter))
            else:
                return stmt.where(getattr(self.model, filter_by).is_(filter))
        return stmt.where(self.model.active.is_(filter))

    def _apply_search(
        self, stmt: Select, search_by: str | None, search: str | None
    ) -> Select:
        """Применяет поиск."""
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
