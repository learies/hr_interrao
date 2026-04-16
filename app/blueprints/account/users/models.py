from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Uuid, func, sql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.settings.database import BaseModel


class UserModel(BaseModel):
    """Модель пользователя."""

    __tablename__ = "user"
    __table_args__ = {"schema": "account"}

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        comment="Идентификатор пользователя",
    )
    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=sql.false(),
        comment="Права администратора",
    )

    # Relationships
    last_login: Mapped["LastLoginModel | None"] = relationship(
        back_populates="user",
        lazy="joined",
    )

    def __repr__(self) -> str:
        """Представление модели в виде строки."""
        class_name = type(self).__name__
        return f"<{class_name}(id={self.id}, is_admin={self.is_admin})>"

    def __str__(self) -> str:
        """Строковое представление модели."""
        return self.__repr__()


class LastLoginModel(BaseModel):
    """Модель последнего входа пользователя."""

    __tablename__ = "last_login"
    __table_args__ = {"schema": "account"}

    user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "account.user.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
        comment="Идентификатор пользователя",
    )
    last_login: Mapped[datetime | None] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        comment="Время последнего входа",
    )

    # Relationships
    user: Mapped["UserModel"] = relationship(
        back_populates="last_login",
        lazy="joined",
    )

    def __repr__(self) -> str:
        """Представление модели в виде строки."""
        class_name = type(self).__name__
        return f"<{class_name}(user_id={self.user_id}, last_login={self.last_login})>"

    def __str__(self) -> str:
        """Строковое представление модели."""
        return self.__repr__()
