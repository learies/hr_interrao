from typing import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.sql.selectable import Select

from ..repositories import ParusRepository
from .models import WorkerModel


class WorkerRepository(ParusRepository[WorkerModel]):
    """Репозиторий для работы с сотрудниками."""

    def get_all(
        self, offset: int, limit: int, active: bool | None
    ) -> Sequence[WorkerModel]:
        """Возвращает всех сотрудников."""
        stmt = select(self.model)
        stmt = self._apply_active(stmt, active)
        return self.session.scalars(stmt.offset(offset).limit(limit)).all()

    def get_by_id(self, id: UUID) -> WorkerModel | None:
        """Возвращает сотрудника по идентификатору."""
        return self.get_by_attribute("id", id)

    def count_all(self, active: bool | None) -> int:
        """Возвращает количество всех сотрудников."""
        stmt = select(func.count()).select_from(self.model)
        stmt = self._apply_active(stmt, active)
        return self.session.scalar(stmt) or 0

    def _apply_active(self, stmt: Select, active: bool | None) -> Select:
        """Применяет фильтр по активности."""
        if active is not None:
            return stmt.where(self.model.active.is_(active))
        return stmt
