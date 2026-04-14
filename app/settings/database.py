from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.session import Session
from sqlalchemy.orm import DeclarativeBase, scoped_session


class BaseModel(DeclarativeBase):
    """Базовая модель для всех моделей."""

    __abstract__ = True


db = SQLAlchemy(model_class=BaseModel)


def get_db_session() -> scoped_session[Session]:
    """Получение сессии для работы с базой данных."""
    return db.session
