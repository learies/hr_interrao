from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Boolean, String, Uuid

from app.settings.database import BaseModel


class WorkerModel(BaseModel):
    """Модель сотрудника."""

    __tablename__ = "worker"
    __bind_key__ = "authorization"

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        comment="Идентификатор сотрудника",
    )
    name: Mapped[str] = mapped_column(
        String,
        comment="Имя сотрудника",
    )
    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        comment="Email сотрудника",
    )
    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        comment="Статус активности сотрудника",
    )

    @property
    def is_active(self) -> bool:
        """Активен ли сотрудник."""
        return self.active

    def __repr__(self) -> str:
        """Представление модели в виде строки."""
        class_name = type(self).__name__
        return f"<{class_name}(id={self.id}, name={self.name}, email={self.email}, active={self.active})>"

    def __str__(self) -> str:
        """Строковое представление модели."""
        return self.__repr__()
