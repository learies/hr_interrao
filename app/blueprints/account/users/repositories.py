from typing import Sequence
from uuid import UUID

from sqlalchemy import select

from ..repositories import AccountRepository
from .models import UserModel


class UserRepository(AccountRepository[UserModel]):
    """Репозиторий для работы с пользователями."""

    def get_all(self) -> Sequence[UserModel]:
        """Возвращает всех пользователей."""
        return self.session.scalars(select(UserModel)).all()

    def get_by_id(self, user_id: UUID) -> UserModel | None:
        """Возвращает пользователя по идентификатору."""
        return self.get_by_attribute("id", user_id)

    def get_by_ids(self, user_ids: Sequence[UUID]) -> Sequence[UserModel]:
        """Возвращает пользователей по идентификаторам."""
        return self.session.scalars(
            select(UserModel).where(UserModel.id.in_(user_ids))
        ).all()
