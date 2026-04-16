from app.core.repositories import BaseRepository
from app.core.types import Model


class AccountRepository(BaseRepository[Model]):
    """Базовый репозиторий для работы с данными из аккаунта."""
