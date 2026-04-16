from typing import Any, Generic, TypeVar

from flask_sqlalchemy.session import Session
from sqlalchemy import select
from sqlalchemy.orm import scoped_session

from app.settings.database import BaseModel

Model = TypeVar("Model", bound=BaseModel)


class AccountRepository(Generic[Model]):
    """Базовый репозиторий."""

    def __init__(self, model: type[Model], session: scoped_session[Session]) -> None:
        """Инициализация репозитория."""
        self.model = model
        self.session = session

    def get_by_attribute(self, attribute: str, value: Any) -> Model | None:
        """Возвращает объект модели по значению указанного атрибута."""
        stmt = select(self.model).where(getattr(self.model, attribute) == value)
        return self.session.scalar(stmt)
