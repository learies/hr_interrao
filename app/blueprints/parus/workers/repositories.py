from typing import Sequence
from uuid import UUID

from sqlalchemy import select

from ..repositories import ParusRepository
from .models import WorkerModel


class WorkerRepository(ParusRepository[WorkerModel]):
    """Репозиторий для работы с сотрудниками."""

    def get_all(self) -> Sequence[WorkerModel]:
        """Возвращает всех сотрудников."""
        return self.session.scalars(select(WorkerModel)).all()

    def get_by_id(self, id: UUID) -> WorkerModel | None:
        """Возвращает сотрудника по идентификатору."""
        return self.get_by_attribute("id", id)
