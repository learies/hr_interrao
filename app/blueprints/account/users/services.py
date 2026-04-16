from uuid import UUID

from app.settings.database import get_db_session

from ..services import AccountService
from .models import UserModel
from .repositories import UserRepository


class UserService(AccountService[UserModel, UserRepository]):
    """Сервис для работы с пользователями."""

    def get_by_id(self, user_id: UUID) -> UserModel | None:
        """Получение пользователя по идентификатору."""
        return self.repository.get_by_id(user_id)


def get_user_service() -> UserService:
    """Получение сервиса для работы с пользователями."""
    session = get_db_session()
    user_repository = UserRepository(UserModel, session)
    return UserService(user_repository)
