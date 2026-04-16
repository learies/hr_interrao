from typing import Generic, TypeVar

from app.settings.database import BaseModel

from .repositories import AccountRepository

Model = TypeVar("Model", bound=BaseModel)
Repository = TypeVar("Repository", bound=AccountRepository)


class AccountService(Generic[Model, Repository]):
    """Базовый сервис."""

    def __init__(self, repository: Repository) -> None:
        """Инициализация сервиса."""
        self.repository = repository
