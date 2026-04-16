from uuid import UUID

from ..repositories import AccountRepository
from .models import UserModel


class UserRepository(AccountRepository[UserModel]):
    """Репозиторий для работы с пользователями."""

    def get_by_id(self, user_id: UUID) -> UserModel | None:
        """Возвращает пользователя по идентификатору."""
        return self.get_by_attribute("id", user_id)
