from app.core.repositories import BaseRepository
from app.core.types import Model


class ParusRepository(BaseRepository[Model]):
    """Базовый репозиторий для работы с данными из ПАРУС."""
