from typing import Sequence
from uuid import UUID

from app.settings.database import get_db_session

from ..services import AccountService
from .dto import UserResponseDTO
from .models import UserModel
from .repositories import UserRepository


class UserService(AccountService[UserModel, UserRepository]):
    """Сервис для работы с пользователями."""

    def _get_response_dto(self, user: UserModel) -> UserResponseDTO:
        """Получение DTO для пользователя."""
        return UserResponseDTO(
            id=user.id,
            is_admin=user.is_admin,
            last_login=user.last_login.last_login if user.last_login else None,
        )

    def get_all(self) -> Sequence[UserResponseDTO]:
        """Получение всех пользователей."""
        users = self.repository.get_all()
        return [self._get_response_dto(user) for user in users]

    def get_by_id(self, user_id: UUID) -> UserResponseDTO | None:
        """Получение пользователя по идентификатору."""
        user = self.repository.get_by_id(user_id)
        return self._get_response_dto(user) if user is not None else None


def get_user_service() -> UserService:
    """Получение сервиса для работы с пользователями."""
    session = get_db_session()
    user_repository = UserRepository(UserModel, session)
    return UserService(user_repository)
