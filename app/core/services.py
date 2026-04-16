from typing import Generic, TypeVar

from .repositories import BaseRepository
from .types import Model

Repository = TypeVar("Repository", bound=BaseRepository)


class BaseService(Generic[Model, Repository]):
    """Базовый сервис."""

    def __init__(self, repository: Repository) -> None:
        """Инициализация сервиса."""
        self.repository = repository
