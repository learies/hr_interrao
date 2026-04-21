from typing import Sequence
from uuid import UUID

from app.settings.database import get_db_session

from ..services import AccountService
from .dto import UserResponseDTO
from .models import UserModel
from .repositories import UserRepository


class UserService(AccountService[UserModel, UserRepository]):
    """Сервис для работы с пользователями."""

    def get_all(self) -> Sequence[UserResponseDTO]:
        """Получение всех пользователей."""
        users = self.repository.get_all()
        return self._build_response_dtos(users)

    def get_by_id(self, user_id: UUID) -> UserResponseDTO | None:
        """Получение пользователя по идентификатору."""
        user = self.repository.get_by_id(user_id)
        return self._build_response_dtos([user])[0] if user else None

    def get_by_ids(self, user_ids: Sequence[UUID]) -> Sequence[UserResponseDTO]:
        """Получение пользователей по идентификаторам."""
        if not user_ids:
            return ()
        users = self.repository.get_by_ids(user_ids)
        return self._build_response_dtos(users)

    def _build_response_dtos(
        self, users: Sequence[UserModel]
    ) -> Sequence[UserResponseDTO]:
        """Получение DTO для пользователя."""
        return [
            UserResponseDTO(
                id=user.id,
                is_admin=user.is_admin,
                last_login=user.last_login.last_login if user.last_login else None,
            )
            for user in users
        ]


def build_user_service() -> UserService:
    """Получение сервиса для работы с пользователями."""
    user_repository = UserRepository(model=UserModel, session=get_db_session())
    return UserService(user_repository)
