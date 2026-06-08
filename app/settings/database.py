from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.session import Session
from sqlalchemy.orm import DeclarativeBase, scoped_session


class _BaseModel(DeclarativeBase):
    """Базовая модель для всех моделей."""

    __abstract__ = True


db = SQLAlchemy(model_class=_BaseModel)

migrate = Migrate(
    compare_type=True, include_schemas=True, version_table_schema="system"
)

BaseModel = db.Model


def get_db_session() -> scoped_session[Session]:
    """Получение сессии для работы с базой данных."""
    return db.session
